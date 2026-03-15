"""
WiFi Communication Module
Handles TCP/WebSocket connection to ESP32
"""
import json
import socket
import logging
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)


class WiFiComm(QThread):
    """
    Thread-safe WiFi communication handler
    Connects to ESP32 via TCP socket
    """
    
    # Signal emitted when new data packet arrives
    data_received = pyqtSignal(dict)
    
    # Signal emitted on connection status change
    connection_status = pyqtSignal(bool, str)
    
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
    def run(self):
        """Main thread loop - reads from TCP socket"""
        self.running = True
        
        try:
            # Create and connect socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(2.0)
            self.socket.connect((self.host, self.port))
            
            logger.info(f"WiFi connected: {self.host}:{self.port}")
            self.connection_status.emit(True, f"Connected to {self.host}")
            
            buffer = ""
            
            # Main read loop
            while self.running:
                try:
                    # Receive data
                    data = self.socket.recv(1024).decode('utf-8')
                    
                    if not data:
                        logger.warning("Connection closed by remote")
                        break
                        
                    buffer += data
                    
                    # Process complete lines (JSON packets)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            try:
                                packet = json.loads(line)
                                self.data_received.emit(packet)
                            except json.JSONDecodeError as e:
                                logger.warning(f"Invalid JSON: {e}")
                                
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"WiFi connection error: {e}")
            self.connection_status.emit(False, f"Error: {str(e)}")
            
        finally:
            if self.socket:
                self.socket.close()
                logger.info("WiFi connection closed")
                
    def stop(self):
        """Stop the communication thread"""
        self.running = False
        self.wait()
