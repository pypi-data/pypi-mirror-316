import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QSlider, QMenuBar, QMenu, QDialog, 
                            QFormLayout, QLineEdit, QPushButton, QFileDialog,
                            QLabel, QComboBox, QMessageBox, QTableView, QInputDialog,
                            QMenu)
from PyQt6.QtCore import (QPoint, Qt, QAbstractTableModel)
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from qtrangeslider import QRangeSlider
from . import nettracer as n3d
from . import smart_dilate
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
from PyQt6.QtGui import (QFont, QCursor)

class ImageViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetTracer3D")
        self.setGeometry(100, 100, 1400, 800)
        
        # Initialize channel data and states
        self.channel_data = [None] * 4
        self.channel_visible = [False] * 4
        self.current_slice = 0
        self.active_channel = 0  # Initialize active channel
        
        # Initialize zoom mode state
        self.zoom_mode = False
        self.original_xlim = None
        self.original_ylim = None

        #Pan mode state
        self.pan_mode = False
        self.panning = False
        self.pan_start = None
        
        # Store brightness/contrast values for each channel
        self.channel_brightness = [{
            'min': 0,
            'max': 1
        } for _ in range(4)]
        
        # Create the brightness dialog but don't show it yet
        self.brightness_dialog = BrightnessContrastDialog(self)
        
        
        # Create control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Create active channel selector
        active_channel_widget = QWidget()
        active_channel_layout = QHBoxLayout(active_channel_widget)
        
        active_label = QLabel("Active Image:")
        active_channel_layout.addWidget(active_label)
        
        self.active_channel_combo = QComboBox()
        self.active_channel_combo.addItems(["Nodes", "Edges", "Network Overlay", "Label Overlay"])
        self.active_channel_combo.setCurrentIndex(0)
        self.active_channel_combo.currentIndexChanged.connect(self.set_active_channel)
        # Initially disable the combo box
        self.active_channel_combo.setEnabled(False)
        active_channel_layout.addWidget(self.active_channel_combo)
        
        control_layout.addWidget(active_channel_widget)

        # Create zoom button and pan button
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)

        # Create zoom button
        self.zoom_button = QPushButton("🔍")
        self.zoom_button.setCheckable(True)
        self.zoom_button.setFixedSize(40, 40)
        self.zoom_button.clicked.connect(self.toggle_zoom_mode)
        control_layout.addWidget(self.zoom_button)

        self.pan_button = QPushButton("✋")
        self.pan_button.setCheckable(True)
        self.pan_button.setFixedSize(40, 40)
        self.pan_button.clicked.connect(self.toggle_pan_mode)
        buttons_layout.addWidget(self.pan_button)

        control_layout.addWidget(buttons_widget)
                
        # Create channel buttons
        self.channel_buttons = []
        self.delete_buttons = []  # New list to store delete buttons
        self.channel_names = ["Nodes", "Edges", "Network Overlay", "Label Overlay"]

        # Create channel toggles with delete buttons
        for i in range(4):
            # Create container for each channel's controls
            channel_container = QWidget()
            channel_layout = QHBoxLayout(channel_container)
            channel_layout.setSpacing(2)  # Reduce spacing between buttons
            
            # Create toggle button
            btn = QPushButton(f"{self.channel_names[i]}")
            btn.setCheckable(True)
            btn.setEnabled(False)
            btn.clicked.connect(lambda checked, ch=i: self.toggle_channel(ch))
            self.channel_buttons.append(btn)
            channel_layout.addWidget(btn)
            
            # Create delete button
            delete_btn = QPushButton("×")  # Using × character for delete
            delete_btn.setFixedSize(20, 20)  # Make it small and square
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: gray;
                    font-weight: bold;
                }
                QPushButton:hover {
                    color: red;
                }
                QPushButton:disabled {
                    color: lightgray;
                }
            """)
            delete_btn.setEnabled(False)
            delete_btn.clicked.connect(lambda checked, ch=i: self.delete_channel(ch))
            self.delete_buttons.append(delete_btn)
            channel_layout.addWidget(delete_btn)
            
            control_layout.addWidget(channel_container)

        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create left panel for image and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create matplotlib canvas for image display
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        left_layout.addWidget(self.canvas)

        
        left_layout.addWidget(control_panel)
        
        # Add slider for depth navigation
        self.slice_slider = QSlider(Qt.Orientation.Horizontal)
        self.slice_slider.setEnabled(False)
        self.slice_slider.valueChanged.connect(self.update_slice)
        left_layout.addWidget(self.slice_slider)
        
        main_layout.addWidget(left_panel)
        
        # Create right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Add matplotlib output window to top right
        self.plot_figure = Figure(figsize=(4, 4))  # Reduced height
        self.plot_canvas = FigureCanvas(self.plot_figure)
        right_layout.addWidget(self.plot_canvas)
        
        # Create table control panel
        table_control = QWidget()
        table_control_layout = QHBoxLayout(table_control)
        
        # Create toggle buttons for tables
        self.network_button = QPushButton("Network")
        self.network_button.setCheckable(True)
        self.network_button.setChecked(True)
        self.network_button.clicked.connect(self.show_network_table)
        
        self.selection_button = QPushButton("Selection")
        self.selection_button.setCheckable(True)
        self.selection_button.clicked.connect(self.show_selection_table)
        
        # Add buttons to control layout
        table_control_layout.addWidget(self.network_button)
        table_control_layout.addWidget(self.selection_button)
        
        # Add control panel to right layout
        right_layout.addWidget(table_control)
        
        # Create both table views
        self.network_table = CustomTableView(self)
        self.selection_table = CustomTableView(self)
        empty_df = pd.DataFrame(columns=['Node 1A', 'Node 1B', 'Edge 1C'])
        self.selection_table.setModel(PandasModel(empty_df))
        self.network_table.setAlternatingRowColors(True)
        self.selection_table.setAlternatingRowColors(True)
        self.network_table.setSortingEnabled(True)
        self.selection_table.setSortingEnabled(True)
        
        # Initially show network table and hide selection table
        right_layout.addWidget(self.network_table)
        right_layout.addWidget(self.selection_table)
        self.selection_table.hide()
        
        # Store reference to currently active table
        self.active_table = self.network_table
        
        main_layout.addWidget(right_panel)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Connect mouse events
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_press_event', self.on_mouse_click)


        # Add these new methods for handling neighbors and components (FOR RIGHT CLICKIGN)
        self.show_neighbors_clicked = None
        self.show_component_clicked = None

        # Initialize highlight overlay
        self.highlight_overlay = None
        self.highlight_bounds = None  # Store bounds for positioning
        
    def create_highlight_overlay(self, node_indices=None, edge_indices=None):
        """
        Create a binary overlay highlighting specific nodes and/or edges using boolean indexing.
        
        Args:
            node_indices (list): List of node indices to highlight
            edge_indices (list): List of edge indices to highlight
        """
        if node_indices is None:
            node_indices = []
        if edge_indices is None:
            edge_indices = []
            
        if not node_indices and not edge_indices:
            self.highlight_overlay = None
            self.highlight_bounds = None
            self.update_display()
            return
            
        # Get the shape of the full array from any existing channel
        for channel in self.channel_data:
            if channel is not None:
                full_shape = channel.shape
                break
        else:
            return  # No valid channels to get shape from
            
        # Initialize full-size overlay
        self.highlight_overlay = np.zeros(full_shape, dtype=np.uint8)
        
        # Add nodes to highlight using boolean indexing
        if node_indices and self.channel_data[0] is not None:
            mask = np.isin(self.channel_data[0], node_indices)
            self.highlight_overlay[mask] = 255
                
        # Add edges to highlight using boolean indexing
        if edge_indices and self.channel_data[1] is not None:
            mask = np.isin(self.channel_data[1], edge_indices)
            self.highlight_overlay[mask] = 255
        
        # Update display
        self.update_display()
    
    def create_context_menu(self, event):
        """Create and show context menu at mouse position."""
        if self.channel_data[self.active_channel] is not None:
            # Convert clicked coordinates to array indices
            x_idx = int(round(event.xdata))
            y_idx = int(round(event.ydata))
            
            try:
                clicked_value = self.channel_data[self.active_channel][self.current_slice, y_idx, x_idx]
                
                # Create context menu
                context_menu = QMenu(self)
                
                # Create "Show Neighbors" submenu
                neighbors_menu = QMenu("Show Neighbors", self)
                
                # Add submenu options
                show_neighbor_nodes = neighbors_menu.addAction("Show Neighboring Nodes")
                show_neighbor_all = neighbors_menu.addAction("Show Neighboring Nodes and Edges")
                
                # Add the submenu to the main context menu
                context_menu.addMenu(neighbors_menu)
                
                # Add "Show Component" action
                show_component = context_menu.addAction("Show Component")
                
                # Store the clicked value and position for use in the callback
                self.show_neighbors_clicked = clicked_value
                self.show_component_clicked = clicked_value
                
                # Store whether we want to show edges too
                self.show_neighbors_with_edges = False
                
                # Connect actions to callbacks
                show_neighbor_nodes.triggered.connect(self.handle_show_neighbors)
                show_neighbor_all.triggered.connect(lambda: self.handle_show_neighbors(edges = True))
                show_component.triggered.connect(self.handle_show_component)
                
                # Get the global position of the cursor
                cursor_pos = QCursor.pos()
                
                # Show context menu at cursor position
                context_menu.exec(cursor_pos)
                
            except IndexError:
                # Clicked outside image boundaries
                pass

    def show_network_table(self):
        """Switch to display the main network table."""
        if not self.network_button.isChecked():
            self.network_button.setChecked(True)
            return
        self.selection_button.setChecked(False)
        self.network_table.show()
        self.selection_table.hide()
        self.active_table = self.network_table

    def show_selection_table(self):
        """Switch to display the selection table."""
        if not self.selection_button.isChecked():
            self.selection_button.setChecked(True)
            return
        self.network_button.setChecked(False)
        self.network_table.hide()
        self.selection_table.show()
        self.active_table = self.selection_table

    def handle_show_neighbors(self, edges=False):
        """Handle the Show Neighbors action."""
        if self.show_neighbors_clicked is not None:
            try:
                # Get neighbors from network
                neighbors = list(my_network.network.neighbors(self.show_neighbors_clicked)) + [self.show_neighbors_clicked]
                
                # Get the existing DataFrame from the model
                original_df = self.network_table.model()._data
                
                # Create mask for rows where either first or second column contains a neighbor
                mask = original_df.iloc[:, 0].isin(neighbors) | original_df.iloc[:, 1].isin(neighbors)
                
                # Filter the DataFrame to only include rows with neighbors
                filtered_df = original_df[mask].copy()
                
                # Create new model with filtered DataFrame and update selection table
                new_model = PandasModel(filtered_df)
                self.selection_table.setModel(new_model)
                
                # Switch to selection table
                self.selection_button.click()
                
                # Create highlight overlay for visualization
                if edges:
                    edge_indices = filtered_df.iloc[:, 2].unique().tolist()
                    self.create_highlight_overlay(node_indices=neighbors, edge_indices=edge_indices)
                else:
                    self.create_highlight_overlay(node_indices=neighbors)
                
                print(f"Found {len(filtered_df)} connections involving node {self.show_neighbors_clicked} and its neighbors")
                
            except Exception as e:
                print(f"Error processing neighbors: {e}")
            
            finally:
                self.show_neighbors_clicked = None

    
    def handle_show_component(self):
        """Handle the Show Component action."""
        if self.show_component_clicked is not None:
            # TODO: Implement show component functionality
            print(f"Show component for value: {self.show_component_clicked}")
            # Will update DataFrame and matplotlib plot
            self.show_component_clicked = None
        
    def toggle_zoom_mode(self):
        """Toggle zoom mode on/off."""
        self.zoom_mode = self.zoom_button.isChecked()
        if self.zoom_mode:
            self.pan_button.setChecked(False)
            self.pan_mode = False
            self.canvas.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.canvas.setCursor(Qt.CursorShape.ArrowCursor)

    def toggle_pan_mode(self):
        """Toggle pan mode on/off."""
        self.pan_mode = self.pan_button.isChecked()
        if self.pan_mode:
            self.zoom_button.setChecked(False)
            self.zoom_mode = False
            self.canvas.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.canvas.setCursor(Qt.CursorShape.ArrowCursor)

    def on_mouse_press(self, event):
        """Handle mouse press events."""
        if event.inaxes != self.ax:
            return
            
        if self.pan_mode:
            self.panning = True
            self.pan_start = (event.xdata, event.ydata)
            self.canvas.setCursor(Qt.CursorShape.ClosedHandCursor)

    def on_mouse_release(self, event):
        """Handle mouse release events."""
        if self.pan_mode:
            self.panning = False
            self.pan_start = None
            self.canvas.setCursor(Qt.CursorShape.OpenHandCursor)

    def on_mouse_move(self, event):
        """Handle mouse movement events."""
        if not self.panning or event.inaxes != self.ax or self.pan_start is None:
            return
            
        # Calculate the movement
        dx = event.xdata - self.pan_start[0]
        dy = event.ydata - self.pan_start[1]
        
        # Get current view limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Calculate new limits
        new_xlim = [xlim[0] - dx, xlim[1] - dx]
        new_ylim = [ylim[0] - dy, ylim[1] - dy]
        
        # Get image bounds
        if self.channel_data[0] is not None:  # Use first channel as reference
            img_height, img_width = self.channel_data[0][self.current_slice].shape
            
            # Ensure new limits don't go beyond image bounds
            if new_xlim[0] < 0:
                new_xlim = [0, xlim[1] - xlim[0]]
            elif new_xlim[1] > img_width:
                new_xlim = [img_width - (xlim[1] - xlim[0]), img_width]
                
            if new_ylim[0] < 0:
                new_ylim = [0, ylim[1] - ylim[0]]
            elif new_ylim[1] > img_height:
                new_ylim = [img_height - (ylim[1] - ylim[0]), img_height]
        
        # Apply new limits
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()
        
        # Update pan start position
        self.pan_start = (event.xdata, event.ydata)


    def highlight_value_in_tables(self, clicked_value):
        """Helper method to find and highlight a value in both tables."""
        
        if not self.network_table.model() and not self.selection_table.model():
            return False

        found = False
        tables_to_check = [self.network_table, self.selection_table]
        active_table_index = tables_to_check.index(self.active_table)
        
        # Reorder tables to check active table first
        tables_to_check = tables_to_check[active_table_index:] + tables_to_check[:active_table_index]
        
        for table in tables_to_check:
            
            if table.model() is None:
                continue
                
            df = table.model()._data

            
            # Create appropriate masks based on active channel
            if self.active_channel == 0:  # Nodes channel
                col1_matches = df[df.columns[0]] == clicked_value
                col2_matches = df[df.columns[1]] == clicked_value
                all_matches = col1_matches | col2_matches

            elif self.active_channel == 1:  # Edges channel
                all_matches = df[df.columns[2]] == clicked_value

            else:
                continue

            if all_matches.any():
                # Get indices from the current dataframe's index
                match_indices = df[all_matches].index.tolist()
                
                # If this is the active table, handle selection and scrolling
                if table == self.active_table:
                    current_row = table.currentIndex().row()
                    
                    # Convert match_indices to row numbers (position in the visible table)
                    row_positions = [df.index.get_loc(idx) for idx in match_indices]
                    
                    # Find next match after current position
                    if current_row >= 0:
                        next_positions = [pos for pos in row_positions if pos > current_row]
                        row_pos = next_positions[0] if next_positions else row_positions[0]
                    else:
                        row_pos = row_positions[0]
                    
                    # Update selection and scroll
                    model_index = table.model().index(row_pos, 0)
                    table.scrollTo(model_index)
                    table.clearSelection()
                    table.selectRow(row_pos)
                    table.setCurrentIndex(model_index)

                
                # Update bold formatting regardless of whether it's the active table
                table.model().set_bold_value(clicked_value, self.active_channel)
                found = True

        return found
        
    def on_mouse_click(self, event):
        """Handle mouse clicks for zooming and data inspection."""
        if event.inaxes != self.ax:
            return
            
        if self.zoom_mode:
            # Existing zoom functionality
            if self.original_xlim is None:
                self.original_xlim = self.ax.get_xlim()
                self.original_ylim = self.ax.get_ylim()
            
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            xdata = event.xdata
            ydata = event.ydata
            
            if event.button == 1:  # Left click - zoom in
                x_range = (current_xlim[1] - current_xlim[0]) / 4
                y_range = (current_ylim[1] - current_ylim[0]) / 4
                
                self.ax.set_xlim([xdata - x_range, xdata + x_range])
                self.ax.set_ylim([ydata - y_range, ydata + y_range])
                
            elif event.button == 3:  # Right click - zoom out
                x_range = (current_xlim[1] - current_xlim[0])
                y_range = (current_ylim[1] - current_ylim[0])
                
                new_xlim = [xdata - x_range, xdata + x_range]
                new_ylim = [ydata - y_range, ydata + y_range]
                
                if (new_xlim[0] <= self.original_xlim[0] or 
                    new_xlim[1] >= self.original_xlim[1] or
                    new_ylim[0] <= self.original_ylim[0] or
                    new_ylim[1] >= self.original_ylim[1]):
                    self.ax.set_xlim(self.original_xlim)
                    self.ax.set_ylim(self.original_ylim)
                else:
                    self.ax.set_xlim(new_xlim)
                    self.ax.set_ylim(new_ylim)
            
            self.canvas.draw()
        
        elif event.button == 3:  # Right click
            self.create_context_menu(event)

        else:  # Not in zoom mode - handle value inspection
            if self.channel_data[self.active_channel] is not None:
                try:
                    # Get clicked value
                    x_idx = int(round(event.xdata))
                    y_idx = int(round(event.ydata))
                    clicked_value = self.channel_data[self.active_channel][self.current_slice, y_idx, x_idx]
                    
                    # Try to find and highlight the value in the current table
                    found = self.highlight_value_in_tables(clicked_value)
                    
                    # If not found in current table but it exists in the other table, offer to switch
                    if not found:
                        other_table = self.selection_table if self.active_table == self.network_table else self.network_table
                        if other_table.model() is not None:
                            df = other_table.model()._data
                            if self.active_channel == 0:
                                exists_in_other = (df[df.columns[0]] == clicked_value).any() or (df[df.columns[1]] == clicked_value).any()
                            else:
                                exists_in_other = (df[df.columns[2]] == clicked_value).any()
                                
                            if exists_in_other:
                                # Switch to the other table
                                if other_table == self.network_table:
                                    self.network_button.click()
                                else:
                                    self.selection_button.click()
                                # Now highlight in the newly active table
                                self.highlight_value_in_tables(clicked_value)
                                
                except IndexError:
                    pass  # Clicked outside image boundaries
                
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")

        # Create Save submenu
        save_menu = file_menu.addMenu("Save")
        network_save = save_menu.addAction("Save Network3D Object")
        network_save.triggered.connect(lambda: self.save_network_3d(False))
        for i in range(4):
            save_action = save_menu.addAction(f"Save {self.channel_names[i]}")
            save_action.triggered.connect(lambda checked, ch=i: self.save(ch, False))

        # Create Save As submenu
        save_as_menu = file_menu.addMenu("Save As")
        network_saveas = save_as_menu.addAction("Save Network3D Object As")
        network_saveas.triggered.connect(lambda: self.save_network_3d(True))
        for i in range(4):
            save_action = save_as_menu.addAction(f"Save {self.channel_names[i]} As")
            save_action.triggered.connect(lambda checked, ch=i: self.save(ch))
        
        # Create Load submenu
        load_menu = file_menu.addMenu("Load")
        network_load = load_menu.addAction("Load Network3D Object")
        network_load.triggered.connect(self.load_from_network_obj)
        for i in range(4):
            load_action = load_menu.addAction(f"Load {self.channel_names[i]}")
            load_action.triggered.connect(lambda checked, ch=i: self.load_channel(ch))

        
        # Analysis menu
        analysis_menu = menubar.addMenu("Analyze")
        netshow_action = analysis_menu.addAction("Show Network")
        netshow_action.triggered.connect(self.show_netshow_dialog)

        # Process menu
        process_menu = menubar.addMenu("Process")
        calc_all_action = process_menu.addAction("Calculate All (Find Node-Edge-Node Network)")
        calc_all_action.triggered.connect(self.show_calc_all_dialog)
        resize_action = process_menu.addAction("Resize (Up/Downsample)")
        resize_action.triggered.connect(self.show_resize_dialog)
        dilate_action = process_menu.addAction("Dilate")
        dilate_action.triggered.connect(self.show_dilate_dialog)
        binarize_action = process_menu.addAction("Binarize")
        binarize_action.triggered.connect(self.show_binarize_dialog)
        watershed_action = process_menu.addAction("Watershed")
        watershed_action.triggered.connect(self.show_watershed_dialog)
        
        # Image menu
        image_menu = menubar.addMenu("Image")
        brightness_action = image_menu.addAction("Adjust Brightness/Contrast")
        brightness_action.triggered.connect(self.show_brightness_dialog)
        show3d_action = image_menu.addAction("Show 3D (beta)")
        show3d_action.triggered.connect(self.show3d_dialog)

    def show_watershed_dialog(self):
        """Show the watershed parameter dialog."""
        dialog = WatershedDialog(self)
        dialog.exec()

    def show_calc_all_dialog(self):
        """Show the calculate all parameter dialog."""
        dialog = CalcAllDialog(self)
        dialog.exec()

    def show_dilate_dialog(self):
        """show the dilate dialog"""
        dialog = DilateDialog(self)
        dialog.exec()

    def show_binarize_dialog(self):
        """show the binarize dialog"""
        dialog = BinarizeDialog(self)
        dialog.exec()


    def show_resize_dialog(self):
        """show the resize dialog"""
        dialog = ResizeDialog(self)
        dialog.exec()
    
    def show_brightness_dialog(self):
        """Show the brightness/contrast control dialog."""
        self.brightness_dialog.show()

    def show3d_dialog(self):
        """Show the 3D control dialog"""
        dialog = Show3dDialog(self)
        dialog.exec()
    

    # Modify load_from_network_obj method
    def load_from_network_obj(self):
        try: 
            directory = QFileDialog.getExistingDirectory(
                self,
                f"Select Directory for Network3D Object",
                "",
                QFileDialog.Option.ShowDirsOnly
            )

            my_network.assemble(directory)

            # Load image channels
            try:
                self.load_channel(0, my_network.nodes, True)
            except Exception as e:
                print(e)
            try:
                self.load_channel(1, my_network.edges, True)
            except Exception as e:
                print(e)
            try:
                self.load_channel(2, my_network.network_overlay, True)
            except Exception as e:
                print(e)
            try:
                self.load_channel(3, my_network.id_overlay, True)
            except Exception as e:
                print(e)

            # Update slider range based on new data
            for channel in self.channel_data:
                if channel is not None:
                    self.slice_slider.setEnabled(True)
                    self.slice_slider.setMinimum(0)
                    self.slice_slider.setMaximum(channel.shape[0] - 1)
                    self.slice_slider.setValue(0)
                    self.current_slice = 0
                    break

            # Display network_lists in the network table
            try:
                if hasattr(my_network, 'network_lists'):
                    model = PandasModel(my_network.network_lists)
                    self.network_table.setModel(model)
                    # Adjust column widths to content
                    for column in range(model.columnCount(None)):
                        self.network_table.resizeColumnToContents(column)
            except Exception as e:
                print(f"Error loading network_lists: {e}")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Loading Network 3D Object",
                f"Failed to load Network 3D Object: {str(e)}"
            )





    def set_active_channel(self, index):
        """Set the active channel and update UI accordingly."""
        self.active_channel = index
        # Update button appearances to show active channel
        for i, btn in enumerate(self.channel_buttons):
            if i == index and btn.isEnabled():
                btn.setStyleSheet("background-color: lightblue;")
            else:
                btn.setStyleSheet("")

    def load_channel(self, channel_index, channel_data=None, data=False):
        """Load a channel and enable active channel selection if needed."""

        try:
            if not data:  # For solo loading
                import tifffile
                filename, _ = QFileDialog.getOpenFileName(
                    self,
                    f"Load Channel {channel_index + 1}",
                    "",
                    "TIFF Files (*.tif *.tiff)"
                )
                self.channel_data[channel_index] = tifffile.imread(filename)
                if channel_index == 0:
                    my_network.nodes = self.channel_data[channel_index]
                elif channel_index == 1:
                    my_network.edges = self.channel_data[channel_index]
                elif channel_index == 2:
                    my_network.network_overlay = self.channel_data[channel_index]
                elif channel_index == 3:
                    my_network.id_overlay = self.channel_data[channel_index]
            else:
                self.channel_data[channel_index] = channel_data
            
            # Enable the channel button
            self.channel_buttons[channel_index].setEnabled(True)
            self.delete_buttons[channel_index].setEnabled(True) 

            
            # Enable active channel selector if this is the first channel loaded
            if not self.active_channel_combo.isEnabled():
                self.active_channel_combo.setEnabled(True)
            
            # Update slider range if this is the first channel loaded
            if not self.slice_slider.isEnabled():
                self.slice_slider.setEnabled(True)
                self.slice_slider.setMinimum(0)
                self.slice_slider.setMaximum(self.channel_data[channel_index].shape[0] - 1)
                self.slice_slider.setValue(0)
                self.current_slice = 0
            
            # If this is the first channel loaded, make it active
            if all(not btn.isEnabled() for btn in self.channel_buttons[:channel_index]):
                self.set_active_channel(channel_index)
            
            self.update_display()
                
        except Exception as e:
            if not data:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self,
                    "Error Loading File",
                    f"Failed to load tiff file: {str(e)}"
                )

    def delete_channel(self, channel_index):
        """Delete the specified channel and update the display."""
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            'Delete Channel',
            f'Are you sure you want to delete the {self.channel_names[channel_index]} channel?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Set channel data to None
            self.channel_data[channel_index] = None
            
            # Update corresponding network property
            if channel_index == 0:
                my_network.nodes = None
            elif channel_index == 1:
                my_network.edges = None
            elif channel_index == 2:
                my_network.network_overlay = None
            elif channel_index == 3:
                my_network.id_overlay = None
            
            # Disable buttons
            self.channel_buttons[channel_index].setEnabled(False)
            self.channel_buttons[channel_index].setChecked(False)
            self.delete_buttons[channel_index].setEnabled(False)
            self.channel_visible[channel_index] = False
            
            # If this was the active channel, switch to the first available channel
            if self.active_channel == channel_index:
                for i in range(4):
                    if self.channel_data[i] is not None:
                        self.set_active_channel(i)
                        break
                else:
                    # If no channels are available, disable active channel selector
                    self.active_channel_combo.setEnabled(False)
            
            # Update display
            self.update_display()


    def save_network_3d(self, asbool = True):

        try:
            if asbool:  # Save As
                # First let user select parent directory
                parent_dir = QFileDialog.getExistingDirectory(
                    self,
                    "Select Location for Network3D Object Outputs",
                    "",
                    QFileDialog.Option.ShowDirsOnly
                )

                if parent_dir:  # If user didn't cancel
                    # Prompt user for new folder name
                    new_folder_name, ok = QInputDialog.getText(
                        self,
                        "New Folder",
                        "Enter name for new output folder:"
                    )
                
            else:  # Save
                parent_dir = None  # Let the backend handle default save location
            
            # Call appropriate save method
            if parent_dir is not None or not asbool:  # Proceed if we have a filename OR if it's a regular save
                if asbool:
                    my_network.dump(parent_dir = parent_dir, name = new_folder_name)
                else:
                    my_network.dump(name = 'my_network')
                
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving File",
                f"Failed to save file: {str(e)}"
            )


    def save(self, ch_index, asbool=True):
        """Handle both Save and Save As operations."""
        try:
            if asbool:  # Save As
                # Open file dialog for saving
                filename, _ = QFileDialog.getSaveFileName(
                    self,
                    f"Save {self.channel_names[ch_index]} As",
                    "",  # Default directory
                    "TIFF Files (*.tif *.tiff);;All Files (*)"  # File type filter
                )
                
                if filename:  # Only proceed if user didn't cancel
                    # If user didn't type an extension, add .tif
                    if not filename.endswith(('.tif', '.tiff')):
                        filename += '.tif'
            else:  # Save
                filename = None  # Let the backend handle default save location
            
            # Call appropriate save method
            if filename is not None or not asbool:  # Proceed if we have a filename OR if it's a regular save
                if ch_index == 0:
                    my_network.save_nodes(filename=filename)
                elif ch_index == 1:
                    my_network.save_edges(filename=filename)
                elif ch_index == 2:
                    my_network.save_network_overlay(filename=filename)
                elif ch_index == 3:
                    my_network.save_id_overlay(filename=filename)
                
                #print(f"Saved {self.channel_names[ch_index]}" + (f" to: {filename}" if filename else ""))  # Debug print
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving File",
                f"Failed to save file: {str(e)}"
            )

    def toggle_channel(self, channel_index):
        """Toggle visibility of a channel."""
        self.channel_visible[channel_index] = self.channel_buttons[channel_index].isChecked()
        self.update_display()
    
    def update_slice(self):
        """Update the current slice when slider moves."""
        self.current_slice = self.slice_slider.value()
        #print(f"Current slice: {self.current_slice}")  # Debug print
        self.update_display()

    def update_brightness(self, channel_index, values):
        """Update brightness/contrast settings for a channel."""
        # Convert slider values (0-100) to data values (0-1)
        min_val, max_val = values
        self.channel_brightness[channel_index]['min'] = min_val / 100
        self.channel_brightness[channel_index]['max'] = max_val / 100
        self.update_display()
    
    def update_display(self):
        """Update the display with currently visible channels and highlight overlay."""
        self.figure.clear()
        
        # Create subplot with tight layout and white figure background
        self.figure.patch.set_facecolor('white')
        self.ax = self.figure.add_subplot(111)
        
        # Store current zoom limits if they exist
        if hasattr(self, 'ax'):
            current_xlim = self.ax.get_xlim() if self.ax.get_xlim() != (0, 1) else None
            current_ylim = self.ax.get_ylim() if self.ax.get_ylim() != (0, 1) else None
        else:
            current_xlim = current_ylim = None
        
        # Define base colors for each channel with increased intensity
        base_colors = [
            (1, 0.3, 0.3),    # Lighter red
            (0.3, 1, 0.3),    # Lighter green
            (1, 1, 1),        # White
            (1, 1, 1)         # White
        ]
        
        # Set only the axes (image area) background to black
        self.ax.set_facecolor('black')
        
        # Display each visible channel
        for channel in range(4):
            if (self.channel_visible[channel] and 
                self.channel_data[channel] is not None):
                current_image = self.channel_data[channel][self.current_slice, :, :]
                
                # Calculate brightness/contrast limits
                img_min = np.min(current_image)
                img_max = np.max(current_image)
                
                # Calculate vmin and vmax, ensuring we don't get a zero range
                if img_min == img_max:
                    # If image is constant, use the value itself
                    vmin = img_min
                    vmax = img_min + 1  # Add 1 to avoid division by zero
                else:
                    vmin = img_min + (img_max - img_min) * self.channel_brightness[channel]['min']
                    vmax = img_min + (img_max - img_min) * self.channel_brightness[channel]['max']
                
                # Normalize the image safely
                if vmin == vmax:
                    normalized_image = np.zeros_like(current_image)
                else:
                    normalized_image = np.clip((current_image - vmin) / (vmax - vmin), 0, 1)
                
                # Create custom colormap with higher intensity
                color = base_colors[channel]
                custom_cmap = LinearSegmentedColormap.from_list(
                    f'custom_{channel}',
                    [(0,0,0,0), (*color,1)]
                )
                
                # Display the image with slightly higher alpha
                self.ax.imshow(normalized_image,
                             alpha=0.7,
                             cmap=custom_cmap,
                             vmin=0,
                             vmax=1)

        # Add highlight overlay if it exists
        if self.highlight_overlay is not None:
            # Get the current slice from the highlight overlay
            highlight_slice = self.highlight_overlay[self.current_slice]
            
            # Create custom colormap for highlight (yellow with transparency)
            highlight_cmap = LinearSegmentedColormap.from_list(
                'highlight',
                [(0, 0, 0, 0), (1, 1, 0, 0.7)]  # Transparent to yellow
            )
            
            # Display highlight
            self.ax.imshow(highlight_slice,
                         cmap=highlight_cmap,
                         alpha=0.5)  # Adjust alpha as needed
        
        # Restore zoom limits if they existed
        if current_xlim is not None and current_ylim is not None:
            self.ax.set_xlim(current_xlim)
            self.ax.set_ylim(current_ylim)
        
        # Style the axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title(f'Slice {self.current_slice}')

        # Make axis labels and ticks black for visibility against white background
        self.ax.xaxis.label.set_color('black')
        self.ax.yaxis.label.set_color('black')
        self.ax.title.set_color('black')
        self.ax.tick_params(colors='black')
        for spine in self.ax.spines.values():
            spine.set_color('black')

        # Adjust the layout to ensure the plot fits well in the figure
        self.figure.tight_layout()
        
        self.canvas.draw()

    def show_netshow_dialog(self):
        dialog = NetShowDialog(self)
        dialog.exec()




#FOR VIEWING: 
class CustomTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.parent = parent  # Store reference to parent window

    def show_context_menu(self, position):
        # Get the index at the clicked position
        index = self.indexAt(position)
        
        if index.isValid():  # Only show menu if we clicked on a valid cell
            # Get the actual data from the model
            model = self.model()
            if model:
                row = index.row()
                column = index.column()
                value = model._data.iloc[row, column]
                
                # Create context menu
                context_menu = QMenu(self)
                find_action = context_menu.addAction("Find")
                
                # Connect the action
                find_action.triggered.connect(lambda: self.handle_find_action(row, column, value))
                
                # Show the menu at cursor position
                cursor_pos = QCursor.pos()
                context_menu.exec(cursor_pos)

    def handle_find_action(self, row, column, value):
        try:
            # Convert value to int if it's not already
            value = int(value)
            
            # Get the currently active table
            active_table = self.parent.active_table
            
            # Determine if we're looking for a node or edge based on column
            if column < 2:  # First two columns are nodes
                if value in my_network.node_centroids:
                    # Get centroid coordinates (Z, Y, X)
                    centroid = my_network.node_centroids[value]
                    # Set the active channel to nodes (0)
                    self.parent.set_active_channel(0)
                    # Toggle on the nodes channel if it's not already visible
                    if not self.parent.channel_visible[0]:
                        self.parent.channel_buttons[0].setChecked(True)
                        self.parent.toggle_channel(0)
                    # Navigate to the Z-slice
                    self.parent.slice_slider.setValue(int(centroid[0]))
                    print(f"Found node {value} at Z-slice {centroid[0]}")
                    self.parent.create_highlight_overlay(node_indices=[value])
                    
                    # Highlight the value in both tables if it exists
                    self.highlight_value_in_table(self.parent.network_table, value, column)
                    self.highlight_value_in_table(self.parent.selection_table, value, column)
                else:
                    print(f"Node {value} not found in centroids dictionary")
                    
            elif column == 2:  # Third column is edges
                if value in my_network.edge_centroids:
                    # Get centroid coordinates (Z, Y, X)
                    centroid = my_network.edge_centroids[value]
                    # Set the active channel to edges (1)
                    self.parent.set_active_channel(1)
                    # Toggle on the edges channel if it's not already visible
                    if not self.parent.channel_visible[1]:
                        self.parent.channel_buttons[1].setChecked(True)
                        self.parent.toggle_channel(1)
                    # Navigate to the Z-slice
                    self.parent.slice_slider.setValue(int(centroid[0]))
                    print(f"Found edge {value} at Z-slice {centroid[0]}")
                    self.parent.create_highlight_overlay(edge_indices=[value])
                    
                    # Highlight the value in both tables if it exists
                    self.highlight_value_in_table(self.parent.network_table, value, column)
                    self.highlight_value_in_table(self.parent.selection_table, value, column)
                else:
                    print(f"Edge {value} not found in centroids dictionary")
                    
        except (ValueError, TypeError) as e:
            print(f"Error processing value: {str(e)}")
            return
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return

    def highlight_value_in_table(self, table, value, column):
        """Helper method to find and highlight a value in a specific table."""
        if table.model() is None:
            return
            
        df = table.model()._data
        
        if column < 2:  # Node
            col1_matches = df[df.columns[0]] == value
            col2_matches = df[df.columns[1]] == value
            all_matches = col1_matches | col2_matches
        else:  # Edge
            all_matches = df[df.columns[2]] == value
        
        if all_matches.any():
            match_indices = all_matches[all_matches].index.tolist()
            row_idx = match_indices[0]
            
            # Only scroll and select if this is the active table
            if table == self.parent.active_table:
                # Create index and scroll to it
                model_index = table.model().index(row_idx, 0)
                table.scrollTo(model_index)
                
                # Select the row
                table.clearSelection()
                table.selectRow(row_idx)
                table.setCurrentIndex(model_index)
            
            # Update bold formatting
            table.model().set_bold_value(value, column < 2 and 0 or 1)




class BrightnessContrastDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Brightness/Contrast Controls")
        self.setModal(False)  # Allows interaction with main window while open
        
        layout = QVBoxLayout(self)
        
        # Create range sliders for each channel
        self.brightness_sliders = []
        for i in range(4):
            channel_widget = QWidget()
            channel_layout = QVBoxLayout(channel_widget)
            
            # Add label
            label = QLabel(f"Channel {i+1} Brightness/Contrast")
            channel_layout.addWidget(label)
            
            # Create range slider
            slider = QRangeSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue((0, 100))
            slider.valueChanged.connect(lambda values, ch=i: self.parent().update_brightness(ch, values))
            self.brightness_sliders.append(slider)
            channel_layout.addWidget(slider)
            
            layout.addWidget(channel_widget)


    #def show_network(self, geometric = False, directory = None):


class NetShowDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Display Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # GPU checkbox (default True)
        self.geo_layout = QPushButton("geo_layout")
        self.geo_layout.setCheckable(True)
        self.geo_layout.setChecked(False)
        layout.addRow("Use Geometric Layout:", self.geo_layout)
        
        # Add Run button
        run_button = QPushButton("Show Network")
        run_button.clicked.connect(self.show_network)
        layout.addWidget(run_button)
    
    def show_network(self):
        # Get parameters and run analysis
        geo = self.geo_layout.isChecked()
        
        try:

            # Example analysis plot
            my_network.show_network(geometric = geo)
            
            self.parent().plot_canvas.draw()
            self.accept()

        except:
            pass

class Show3dDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Display Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)

        self.downsample = QLineEdit("1")
        layout.addRow("Downsample Factor (Expect Slowness on Large Images):", self.downsample)

        # Network Overlay checkbox (default True)
        self.overlay = QPushButton("Network Overlay")
        self.overlay.setCheckable(True)
        self.overlay.setChecked(True)
        layout.addRow("Include Network Overlay", self.overlay)
        
        # Add Run button
        run_button = QPushButton("Show 3D")
        run_button.clicked.connect(self.show_3d)
        layout.addWidget(run_button)


    def show_3d(self):

        try:
            
            # Get amount
            try:
                downsample = float(self.downsample.text()) if self.downsample.text() else 1
            except ValueError:
                downsample = 1

            overlay = self.overlay.isChecked()
            if overlay:
        
                # Example analysis plot
                my_network.show_3D(my_network.network_overlay, downsample)
            else:
                my_network.show_3D(down_factor = downsample)
            
            self.accept()

        except Exception as e:
            print(f"Error: {e}")





# MISC DISPLAY FUNCTIONS:

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        if type(data) == list:
            data = self.lists_to_dataframe(data[0], data[1], data[2], column_names=['Node 1A', 'Node 1B', 'Edge 1C'])
        self._data = data
        self.bold_cells = set()  # Store (index, col) pairs that should be bold

    @staticmethod
    def lists_to_dataframe(list1, list2, list3, column_names=['Column1', 'Column2', 'Column3']):
        """
        Convert three lists into a pandas DataFrame with specified column names.
        
        Parameters:
        list1, list2, list3: Lists of equal length
        column_names: List of column names (default provided)
        
        Returns:
        pandas.DataFrame: DataFrame with three columns
        """
        df = pd.DataFrame({
            column_names[0]: list1,
            column_names[1]: list2,
            column_names[2]: list3
        })
        return df

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        elif role == Qt.ItemDataRole.FontRole:
            # Get the actual index from the DataFrame for this row
            df_index = self._data.index[index.row()]
            if (df_index, index.column()) in self.bold_cells:
                font = QFont()
                font.setBold(True)
                return font
        return None
    
    def set_bold_value(self, value, active_channel=0):
        """Set bold formatting for cells containing this value in relevant columns based on active channel"""
        print(f"Setting bold for value {value} in table with shape {self._data.shape}")
        # Clear previous bold cells
        self.bold_cells.clear()
        
        if active_channel == 0:
            # For nodes, search first two columns
            for col in [0, 1]:
                matches = self._data.iloc[:, col] == value
                for idx in matches[matches].index:
                    self.bold_cells.add((idx, col))
                    print(f"Added bold cell: index {idx}, column {col}")
        elif active_channel == 1:
            # For edges, only search third column
            matches = self._data.iloc[:, 2] == value
            for idx in matches[matches].index:
                self.bold_cells.add((idx, 2))
                print(f"Added bold cell: index {idx}, column 2")
        
        # Emit signal to refresh the view
        self.layoutChanged.emit()
        print(f"Bold cells after update: {self.bold_cells}")

# MISC ANALYSIS FUNCTIONS:


class ResizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)
        self.resize = QLineEdit()
        self.resize.setPlaceholderText("Will Override Below")
        layout.addRow("Resize Factor (All Dimensions):", self.resize)
        self.zsize = QLineEdit("1")
        layout.addRow("Resize Z Factor:", self.zsize)
        self.ysize = QLineEdit("1")
        layout.addRow("Resize Y Factor:", self.ysize)
        self.xsize = QLineEdit("1")
        layout.addRow("Resize X Factor:", self.xsize)


        # cubic checkbox (default False)
        self.cubic = QPushButton("Use Cubic Resize? (Will alter labels and require re-binarization -> labelling, but preserves shape better)")
        self.cubic.setCheckable(True)
        self.cubic.setChecked(False)
        layout.addRow("Use cubic algorithm:", self.cubic)
        
        
        run_button = QPushButton("Run Resize")
        run_button.clicked.connect(self.run_resize)
        layout.addRow(run_button)

    def reset_fields(self):
        """Reset all input fields to default values"""
        self.resize.clear()
        self.zsize.setText("1")
        self.xsize.setText("1")
        self.ysize.setText("1")

    def run_resize(self):
        try:
            # Get amount
            try:
                resize = float(self.resize.text()) if self.resize.text() else None
                zsize = float(self.zsize.text()) if self.zsize.text() else 1
                ysize = float(self.ysize.text()) if self.ysize.text() else 1
                xsize = float(self.xsize.text()) if self.xsize.text() else 1
            except ValueError as e:
                print(f"Invalid input value: {e}")
                self.reset_fields()
                return
            
            resize = resize if resize is not None else (zsize, ysize, xsize)
            
            # Get the shape from whichever array exists
            array_shape = None
            if my_network.nodes is not None:
                array_shape = my_network.nodes.shape
            elif my_network.edges is not None:
                array_shape = my_network.edges.shape
            elif my_network.network_overlay is not None:
                array_shape = my_network.network_overlay.shape
            elif my_network.id_overlay is not None:
                array_shape = my_network.id_overlay.shape
                
            if array_shape is None:
                QMessageBox.critical(self, "Error", "No valid array found to resize")
                self.reset_fields()
                return
                
            # Check if resize would result in valid dimensions
            if isinstance(resize, (int, float)):
                new_shape = tuple(int(dim * resize) for dim in array_shape)
            else:
                new_shape = tuple(int(dim * factor) for dim, factor in zip(array_shape, resize))
                
            if any(dim < 1 for dim in new_shape):
                QMessageBox.critical(self, "Error", f"Resize would result in invalid dimensions: {new_shape}")
                self.reset_fields()
                return

            cubic = self.cubic.isChecked()
            if cubic:
                order = 3
            else:
                order = 0
                
            # If checks pass, proceed with resize
            if my_network.nodes is not None:
                my_network.nodes = n3d.resize(my_network.nodes, resize, order)
            if my_network.edges is not None:
                my_network.edges = n3d.resize(my_network.edges, resize, order)
            if my_network.network_overlay is not None:
                my_network.network_overlay = n3d.resize(my_network.network_overlay, resize, order)
            if my_network.id_overlay is not None:
                my_network.id_overlay = n3d.resize(my_network.id_overlay, resize, order)
                
            # Resize highlight overlay if it exists
            parent_window = self.parent()
            if parent_window is not None and parent_window.highlight_overlay is not None:
                parent_window.highlight_overlay = n3d.resize(parent_window.highlight_overlay, resize, order)
                    
            self.parent().channel_data[0] = my_network.nodes
            self.parent().channel_data[1] = my_network.edges
            self.parent().channel_data[2] = my_network.network_overlay
            self.parent().channel_data[3] = my_network.id_overlay
            self.parent().update_display()
            self.reset_fields()
            self.accept()
            
        except Exception as e:
            print(f"Error during resize operation: {e}")
            self.reset_fields()
            QMessageBox.critical(self, "Error", f"Failed to resize: {str(e)}")


class BinarizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Binarize Active Channel?")
        self.setModal(True)
        
        layout = QFormLayout(self)

       # Add Run button
        run_button = QPushButton("Run Binarize")
        run_button.clicked.connect(self.run_binarize)
        layout.addRow(run_button)

    def run_binarize(self):

        # Get the active channel data from parent
        active_data = self.parent().channel_data[self.parent().active_channel]
        if active_data is None:
            raise ValueError("No active image selected")

        try:
            # Call watershed method with parameters
            result = n3d.binarize(
                active_data
                )

            # Update both the display data and the network object
            self.parent().channel_data[self.parent().active_channel] = result


            # Update the corresponding property in my_network
            setattr(my_network, network_properties[self.parent().active_channel], result)

            self.parent().update_display()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error running binarize: {str(e)}"
            )




class DilateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dilate Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)

        self.amount = QLineEdit("1")
        layout.addRow("Dilation Radius:", self.amount)

        if my_network.xy_scale is not None:
            xy_scale = f"{my_network.xy_scale}"
        else:
            xy_scale = "1"

        self.xy_scale = QLineEdit(xy_scale)
        layout.addRow("xy_scale:", self.xy_scale)

        if my_network.z_scale is not None:
            z_scale = f"{my_network.z_scale}"
        else:
            z_scale = "1"

        self.z_scale = QLineEdit(z_scale)
        layout.addRow("z_scale:", self.z_scale)

       # Add Run button
        run_button = QPushButton("Run Dilate")
        run_button.clicked.connect(self.run_dilate)
        layout.addRow(run_button)

    def run_dilate(self):
        try:
            
            # Get amount
            try:
                amount = float(self.amount.text()) if self.amount.text() else 1
            except ValueError:
                amount = 1

            try:
                xy_scale = float(self.xy_scale.text()) if self.xy_scale.text() else 1
            except ValueError:
                xy_scale = 1

            try:
                z_scale = float(self.z_scale.text()) if self.z_scale.text() else 1
            except ValueError:
                z_scale = 1
            
            # Get the active channel data from parent
            active_data = self.parent().channel_data[self.parent().active_channel]
            if active_data is None:
                raise ValueError("No active image selected")
            
            # Call dilate method with parameters
            result = n3d.dilate(
                active_data,
                amount,
                xy_scale = xy_scale,
                z_scale = z_scale,
            )

            # Update both the display data and the network object
            self.parent().channel_data[self.parent().active_channel] = result


            # Update the corresponding property in my_network
            setattr(my_network, network_properties[self.parent().active_channel], result)

            self.parent().update_display()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error running dilate: {str(e)}"
            )


class WatershedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Watershed Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # Directory (empty by default)
        self.directory = QLineEdit()
        self.directory.setPlaceholderText("Leave empty for None")
        layout.addRow("Output Directory:", self.directory)
        
        # Proportion (default 0.1)
        self.proportion = QLineEdit("0.1")
        layout.addRow("Proportion:", self.proportion)
        
        # GPU checkbox (default True)
        self.gpu = QPushButton("GPU")
        self.gpu.setCheckable(True)
        self.gpu.setChecked(True)
        layout.addRow("Use GPU:", self.gpu)
        
        # Smallest radius (empty by default)
        self.smallest_rad = QLineEdit()
        self.smallest_rad.setPlaceholderText("Leave empty for None")
        layout.addRow("Smallest Radius:", self.smallest_rad)
        
        # Predownsample (empty by default)
        self.predownsample = QLineEdit()
        self.predownsample.setPlaceholderText("Leave empty for None")
        layout.addRow("Smart Dilate GPU Downsample:", self.predownsample)
        
        # Predownsample2 (empty by default)
        self.predownsample2 = QLineEdit()
        self.predownsample2.setPlaceholderText("Leave empty for None")
        layout.addRow("Smart Label GPU Downsample:", self.predownsample2)
        
        # Add Run button
        run_button = QPushButton("Run Watershed")
        run_button.clicked.connect(self.run_watershed)
        layout.addRow(run_button)

    def run_watershed(self):
        try:
            # Get directory (None if empty)
            directory = self.directory.text() if self.directory.text() else None
            
            # Get proportion (0.1 if empty or invalid)
            try:
                proportion = float(self.proportion.text()) if self.proportion.text() else 0.1
            except ValueError:
                proportion = 0.1
            
            # Get GPU state
            gpu = self.gpu.isChecked()
            
            # Get smallest_rad (None if empty)
            try:
                smallest_rad = float(self.smallest_rad.text()) if self.smallest_rad.text() else None
            except ValueError:
                smallest_rad = None
            
            # Get predownsample (None if empty)
            try:
                predownsample = float(self.predownsample.text()) if self.predownsample.text() else None
            except ValueError:
                predownsample = None
            
            # Get predownsample2 (None if empty)
            try:
                predownsample2 = float(self.predownsample2.text()) if self.predownsample2.text() else None
            except ValueError:
                predownsample2 = None
            
            # Get the active channel data from parent
            active_data = self.parent().channel_data[self.parent().active_channel]
            if active_data is None:
                raise ValueError("No active image selected")
            
            # Call watershed method with parameters
            result = n3d.watershed(
                active_data,
                directory=directory,
                proportion=proportion,
                GPU=gpu,
                smallest_rad=smallest_rad,
                predownsample=predownsample,
                predownsample2=predownsample2
            )

            # Update both the display data and the network object
            self.parent().channel_data[self.parent().active_channel] = result


            # Update the corresponding property in my_network
            setattr(my_network, network_properties[self.parent().active_channel], result)

            self.parent().update_display()
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error running watershed: {str(e)}"
            )


class CalcAllDialog(QDialog):
    # Class variables to store previous settings
    prev_directory = ""
    prev_xy_scale = "1"
    prev_z_scale = "1"
    prev_search = ""
    prev_diledge = ""
    prev_down_factor = ""
    prev_GPU_downsample = ""
    prev_other_nodes = ""
    prev_remove_trunk = ""
    prev_gpu = True
    prev_label_nodes = True
    prev_inners = True
    prev_skeletonize = False
    prev_overlays = True
    prev_updates = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculate All Parameters")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # Directory (empty by default)
        self.directory = QLineEdit(self.prev_directory)
        self.directory.setPlaceholderText("Leave empty for 'my_network'")
        layout.addRow("Output Directory:", self.directory)
        
        # Load previous values for all inputs
        self.xy_scale = QLineEdit(self.prev_xy_scale)
        layout.addRow("xy_scale:", self.xy_scale)
        
        self.z_scale = QLineEdit(self.prev_z_scale)
        layout.addRow("z_scale:", self.z_scale)

        self.search = QLineEdit(self.prev_search)
        self.search.setPlaceholderText("Leave empty for None")
        layout.addRow("Node Search (float):", self.search)

        self.diledge = QLineEdit(self.prev_diledge)
        self.diledge.setPlaceholderText("Leave empty for None")
        layout.addRow("Edge Reconnection Distance (int):", self.diledge)

        self.down_factor = QLineEdit(self.prev_down_factor)
        self.down_factor.setPlaceholderText("Leave empty for None")
        layout.addRow("Downsample for Centroids (int):", self.down_factor)

        self.GPU_downsample = QLineEdit(self.prev_GPU_downsample)
        self.GPU_downsample.setPlaceholderText("Leave empty for None")
        layout.addRow("Downsample for Distance Transform (GPU) (int):", self.GPU_downsample)

        self.other_nodes = QLineEdit(self.prev_other_nodes)
        self.other_nodes.setPlaceholderText("Leave empty for None")
        layout.addRow("Filepath or directory containing additional node images:", self.other_nodes)

        self.remove_trunk = QLineEdit(self.prev_remove_trunk)
        self.remove_trunk.setPlaceholderText("Leave empty for 0")
        layout.addRow("Times to remove edge trunks (int): ", self.remove_trunk)

        # Load previous button states
        self.gpu = QPushButton("GPU")
        self.gpu.setCheckable(True)
        self.gpu.setChecked(self.prev_gpu)
        layout.addRow("Use GPU:", self.gpu)

        self.label_nodes = QPushButton("Label")
        self.label_nodes.setCheckable(True)
        self.label_nodes.setChecked(self.prev_label_nodes)
        layout.addRow("Label Nodes:", self.label_nodes)

        self.inners = QPushButton("Inner Edges")
        self.inners.setCheckable(True)
        self.inners.setChecked(self.prev_inners)
        layout.addRow("Use Inner Edges:", self.inners)

        self.skeletonize = QPushButton("Skeletonize")
        self.skeletonize.setCheckable(True)
        self.skeletonize.setChecked(self.prev_skeletonize)
        layout.addRow("Skeletonize Edges:", self.skeletonize)

        self.overlays = QPushButton("Overlays")
        self.overlays.setCheckable(True)
        self.overlays.setChecked(self.prev_overlays)
        layout.addRow("Generate Overlays:", self.overlays)

        self.update = QPushButton("Update")
        self.update.setCheckable(True)
        self.update.setChecked(self.prev_updates)
        layout.addRow("Update Node/Edge in NetTracer3D:", self.update)
        
        # Add Run button
        run_button = QPushButton("Run Calculate All")
        run_button.clicked.connect(self.run_calc_all)
        layout.addRow(run_button)

    def run_calc_all(self):

        try:
            # Get directory (None if empty)
            directory = self.directory.text() if self.directory.text() else None
            
            # Get xy_scale and z_scale (1 if empty or invalid)
            try:
                xy_scale = float(self.xy_scale.text()) if self.xy_scale.text() else 1
            except ValueError:
                xy_scale = 1
                
            try:
                z_scale = float(self.z_scale.text()) if self.z_scale.text() else 1
            except ValueError:
                z_scale = 1
            
            # Get search value (None if empty)
            try:
                search = float(self.search.text()) if self.search.text() else None
            except ValueError:
                search = None
                
            # Get diledge value (None if empty)
            try:
                diledge = int(self.diledge.text()) if self.diledge.text() else None
            except ValueError:
                diledge = None
                
            # Get down_factor value (None if empty)
            try:
                down_factor = int(self.down_factor.text()) if self.down_factor.text() else None
            except ValueError:
                down_factor = None
                
            # Get GPU_downsample value (None if empty)
            try:
                GPU_downsample = int(self.GPU_downsample.text()) if self.GPU_downsample.text() else None
            except ValueError:
                GPU_downsample = None
                
            # Get other_nodes path (None if empty)
            other_nodes = self.other_nodes.text() if self.other_nodes.text() else None
            
            # Get remove_trunk value (0 if empty)
            try:
                remove_trunk = int(self.remove_trunk.text()) if self.remove_trunk.text() else 0
            except ValueError:
                remove_trunk = 0
                
            # Get button states
            gpu = self.gpu.isChecked()
            label_nodes = self.label_nodes.isChecked()
            inners = self.inners.isChecked()
            skeletonize = self.skeletonize.isChecked()
            overlays = self.overlays.isChecked()
            update = self.update.isChecked()

            if not update:
                temp_nodes = my_network.nodes.copy()
                temp_edges = my_network.edges.copy()
            
            my_network.calculate_all(
                my_network.nodes,
                my_network.edges,
                directory=directory,
                xy_scale=xy_scale,
                z_scale=z_scale,
                search=search,
                diledge=diledge,
                down_factor=down_factor,
                GPU_downsample=GPU_downsample,
                other_nodes=other_nodes,
                remove_trunk=remove_trunk,
                GPU=gpu,
                label_nodes=label_nodes,
                inners=inners,
                skeletonize=skeletonize
            )

            # Store current values as previous values
            CalcAllDialog.prev_directory = self.directory.text()
            CalcAllDialog.prev_xy_scale = self.xy_scale.text()
            CalcAllDialog.prev_z_scale = self.z_scale.text()
            CalcAllDialog.prev_search = self.search.text()
            CalcAllDialog.prev_diledge = self.diledge.text()
            CalcAllDialog.prev_down_factor = self.down_factor.text()
            CalcAllDialog.prev_GPU_downsample = self.GPU_downsample.text()
            CalcAllDialog.prev_other_nodes = self.other_nodes.text()
            CalcAllDialog.prev_remove_trunk = self.remove_trunk.text()
            CalcAllDialog.prev_gpu = self.gpu.isChecked()
            CalcAllDialog.prev_label_nodes = self.label_nodes.isChecked()
            CalcAllDialog.prev_inners = self.inners.isChecked()
            CalcAllDialog.prev_skeletonize = self.skeletonize.isChecked()
            CalcAllDialog.prev_overlays = self.overlays.isChecked()
            CalcAllDialog.prev_updates = self.update.isChecked()


            # Update both the display data and the network object
            if update:
                self.parent().channel_data[0] = my_network.nodes
                self.parent().channel_data[1] = my_network.edges
            else:
                my_network.nodes = temp_nodes.copy()
                del temp_nodes
                my_network.edges = temp_edges.copy()
                del temp_edges
                self.parent().channel_data[0] = my_network.nodes
                self.parent().channel_data[1] = my_network.edges


            # Then handle overlays
            if overlays:
                if directory is None:
                    directory = 'my_network'
                
                # Generate and update overlays
                my_network.network_overlay = my_network.draw_network(directory=directory)
                my_network.id_overlay = my_network.draw_node_indices(directory=directory)
                
                # Update channel data
                self.parent().channel_data[2] = my_network.network_overlay
                self.parent().channel_data[3] = my_network.id_overlay
                
                # Enable the overlay channel buttons
                self.parent().channel_buttons[2].setEnabled(True)
                self.parent().channel_buttons[3].setEnabled(True)


            self.parent().update_display()
            self.accept()

            # Display network_lists in the network table
            try:
                if hasattr(my_network, 'network_lists'):
                    model = PandasModel(my_network.network_lists)
                    self.parent().network_table.setModel(model)
                    # Adjust column widths to content
                    for column in range(model.columnCount(None)):
                        self.parent().network_table.resizeColumnToContents(column)
            except Exception as e:
                print(f"Error loading network_lists: {e}")

            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error running calculate all: {str(e)}"
            )







if __name__ == '__main__':
    global my_network
    my_network = n3d.Network_3D()
    global network_properties
    # Update the corresponding network property based on active channel
    network_properties = {
        0: 'nodes',
        1: 'edges',
        2: 'network_overlay',
        3: 'id_overlay'
    }

    app = QApplication(sys.argv)
    window = ImageViewerWindow()
    window.show()
    sys.exit(app.exec())