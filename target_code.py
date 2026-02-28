import sqlite3

# --- Database setup and query execution ---

def get_db_connection():
    """
    Establishes an in-memory SQLite connection for demonstration purposes.
    Initializes the 'users' table and adds a sample user if they don't exist.
    In a real application, you would connect to a persistent database (e.g., PostgreSQL, MySQL).
    """
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON;') # Optional: Enable foreign keys

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')

    # Add a sample user for testing authentication
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('validuser', 'securepassword123'))
        conn.commit()
    except sqlite3.IntegrityError:
        # 'validuser' already exists, which is expected on subsequent calls to get_db_connection
        pass

    return conn

def execute_db_query(query: str, params: tuple = None):
    """
    Executes a database query using parameterized queries to prevent SQL injection.
    Manages connection lifecycle: opens, executes, fetches/commits, and closes.
    Returns fetched rows for SELECT queries, or rowcount for DML statements.
    Raises sqlite3.Error on database errors.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Determine if it's a SELECT query to fetch results
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            conn.commit()
            return cursor.rowcount # For INSERT, UPDATE, DELETE

    except sqlite3.Error as e:
        # In a real application, you would log the specific error details here.
        if conn:
            conn.rollback() # Ensure transaction is rolled back on error
        raise # Re-raise the exception after logging for upstream handling
    finally:
        if conn:
            conn.close()

# --- Authenticate User function (fixed with parameterized queries) ---

def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates a user by checking their username and password against the database.
    Uses parameterized queries to prevent SQL injection vulnerabilities.
    Returns True on successful authentication, False otherwise.
    """
    # Use '?' as a placeholder for parameters (standard for sqlite3).
    # For other database APIs, this might be '%s' (e.g., psycopg2, MySQLdb)
    # or ':param_name' (e.g., cx_Oracle).
    query = "SELECT id FROM users WHERE username = ? AND password = ?"

    try:
        # Pass the username and password as a tuple of parameters to the execute_db_query function.
        # The database driver will handle proper escaping of these values,
        # treating them as literal strings rather than executable SQL code,
        # thus preventing SQL injection.
        results = execute_db_query(query, (username, password))

        # If the results list is not empty, it means a matching user was found.
        # The boolean conversion handles both empty list (False) and non-empty list (True).
        return bool(results)

    except Exception:
        # Catch any broader exceptions during database interaction (e.g., connection issues,
        # unexpected query errors from execute_db_query).
        # In a real application, you would log the exception details for debugging.
        return False