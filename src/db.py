import sqlite3

class WellRepository:
    """
    Repository class to interact with the SQLite database of well data
    """
    def __init__(self) -> None:
        self._conn = sqlite3.connect('wells.db', check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._init_table()

    def _init_table(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_well_data (
                "Operator" TEXT,
                "Status" TEXT,
                "Well Type" TEXT,
                "Work Type" TEXT,
                "Directional Status" TEXT,
                "Multi-Lateral" BOOLEAN,
                "Mineral Owner" TEXT,
                "Surface Owner" TEXT,
                "Surface Location" TEXT,
                "GL Elevation" REAL,
                "KB Elevation" REAL,
                "DF Elevation" REAL,
                "Single/Multiple Completion" TEXT,
                "Potash Waiver" BOOLEAN,
                "Spud Date" DATE,
                "Last Inspection" DATE,
                "TVD" REAL,
                "API" TEXT,
                "Latitude" REAL,
                "Longitude" REAL,
                "CRS" TEXT
            );
        ''')
        self._conn.commit()

    def insert(self, model: dict) -> None:
        # dynamically generate the SQL query based on the model
        keys = ', '.join(f'"{key}"' for key in model.keys())
        placeholders = ', '.join('?' for _ in model)

        query = f'INSERT INTO api_well_data ({keys}) VALUES ({placeholders})'
        self._cursor.execute(query, tuple(model.values()))
        self._conn.commit()

    def get_well(self, api: str) -> dict:
        self._cursor.execute('SELECT * FROM api_well_data WHERE "API" = ?', (api,))
        result = self._cursor.fetchone()
        return dict(result) if result else None

    def get_all_coords(self) -> list:
        query = '''
            SELECT "API", "Latitude", "Longitude" FROM api_well_data
        '''
        self._cursor.execute(query)
        return [dict(x) for x in self._cursor.fetchall()]
