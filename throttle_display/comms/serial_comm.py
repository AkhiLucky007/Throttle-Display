"""
Serial Communication Module
Handles USB serial connection to ESP32/Arduino
"""
import json
import logging
import serial
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)


class SerialComm(QThread):
    """
    Thread-safe serial communication handler
    Reads JSON-formatted data packets from embedded device
    """
    
    # Signal emitted when new data packet arrives
    data_received = pyqtSignal(dict)
    
    # Signal emitted on connection status change
    connection_status = pyqtSignal(bool, str)  # (connected, message)
    
    def __init__(self, port, baudrate=115200, timeout=1.0):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.running = False
        
    def run(self):
        """Main thread loop - reads from serial port"""
        self.running = True
        
        try:
            # Open serial connection
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            logger.info(f"Serial port opened: {self.port} @ {self.baudrate} baud")
            self.connection_status.emit(True, f"Connected to {self.port}")
            
            # Main read loop
            while self.running:
                try:
                    # Read line (expecting JSON per line)
                    if self.serial_conn.in_waiting:
                        line = self.serial_conn.readline().decode('utf-8').strip()
                        
                        if line:
                            # Parse JSON data
                            data = json.loads(line)
                            self.data_received.emit(data)
                            
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON received: {e}")
                except UnicodeDecodeError as e:
                    logger.warning(f"Invalid UTF-8 data: {e}")
                    
        except serial.SerialException as e:
            logger.error(f"Serial port error: {e}")
            self.connection_status.emit(False, f"Error: {str(e)}")
            
        finally:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
                logger.info("Serial port closed")
                
    def stop(self):
        """Stop the communication thread"""
        self.running = False
        self.wait()  # Wait for thread to finish
