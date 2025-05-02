import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from contextlib import contextmanager
from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk

# Database configuration
dbconfig = {
    "host": "141.209.241.57",
    "user": "chaga1c",
    "password": "mypass",
    "database": "BIS698W1700_GRP12"
}

class DBAccess:
    pool = MySQLConnectionPool(pool_name="carpool_pool", pool_size=5, **dbconfig)

    @classmethod
    @contextmanager
    def get_connection(cls):
        """Context manager for connection handling with automatic return to pool"""
        conn = cls.pool.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def execute_query(query, params=None):
        """For SELECT queries with automatic connection management"""
        with DBAccess.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    @staticmethod
    def execute_update(query, params=None):
        """For INSERT/UPDATE/DELETE operations with transaction handling"""
        with DBAccess.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
                except Exception as e:
                    conn.rollback()
                    raise e

def resize_image(size, path):
    """Image resizing helper"""
    return ImageTk.PhotoImage(Image.open(path).resize(size))

def centre_window(window):
    """Center the window on screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')