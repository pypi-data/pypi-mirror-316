import copy
import logging
import time
from urllib.parse import urlparse

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session

from database_helper.database.constants_conn import MAX_CONNECTIONS, MIN_CONNECTIONS
from database_helper.database.model_mappings import model_mapping


class SyncDatabaseDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SyncDatabaseDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string=None, db_type=None, config_obj=None,
                 pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS, logger=None):
        if not hasattr(self, "initialized"):
            self.connection_string = connection_string
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.engine: Engine = None
            self.Session = None
            self.tables = {}
            self.engines = {}  # Cache to hold connections for each database
            self.current_db = self.extract_dbname()  # Store the extracted db name
            self.initialized = True
            self.logger = logger or logging.getLogger(__name__)  # Use provided logger or create a new one

    def __enter__(self):
        if not self.engine:
            self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()
        self.engine.dispose()

    def extract_dbname(self):
        """
        Extract the database name from the connection string.
        Assumes the connection string is in the format '.../dbname?...'.
        """
        try:
            # Split the connection string to get the database name
            parsed_url = urlparse(self.connection_string)
            dbname = parsed_url.path.strip('/')  # Remove leading '/'
            return dbname
        except Exception as e:
            self.logger.error(f"Error extracting database name: {e}")
            return None  # Fallback if dbname extraction fails

    def connect(self, dbname=None):
        """
        Connects to the specified database. If no database is provided, connects using the default connection string.
        """
        try:
            # If switching databases, update the connection string dynamically
            if dbname:
                if dbname in self.engines:
                    # Reuse the existing engine for this database
                    self.engine = self.engines[dbname]
                else:
                    # Construct new connection string with the new database name
                    connection_string = self.connection_string.replace(self.current_db,
                                                                       dbname) if self.current_db else self.connection_string
                    self.engine = create_engine(
                        connection_string,
                        pool_size=self.pool_size,
                        max_overflow=self.max_overflow,
                        pool_recycle=3600
                    )
                    self.engines[dbname] = self.engine
                    self.current_db = dbname
            else:
                # If no dbname is provided, use the default connection
                self.engine = create_engine(
                    self.connection_string,
                    pool_size=self.pool_size,
                    max_overflow=self.max_overflow,
                    pool_recycle=3600
                )
                self.engines[self.current_db] = self.engine

            self.Session = scoped_session(sessionmaker(bind=self.engine))
            self.logger.info(f'Database connected: {self.current_db or dbname}')
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")

    def disconnect(self):
        """
        Dispose of the engine, closing all connections.
        """
        if self.engine:
            self.Session.close()
            self.engine.dispose()
            self.logger.info(f'Database {self.current_db} disconnected')
            if self.Session:
                self.Session.remove()

    def switch_database(self, dbname):
        """
        Switches to the provided database if not already connected.
        Creates a new engine for the new database if it's not already cached.
        """
        if self.current_db == dbname:
            self.logger.info(f"Already connected to {dbname}")
            return

        self.logger.info(f"Switching to database {dbname}")
        self.connect(dbname)

    def initialize_tables(self, table_names, dbname=None):
        """
        Initializes metadata for tables. Optionally, it can switch databases before initializing tables.
        """
        try:
            if dbname:
                self.switch_database(dbname)  # Switch the database if required
            if not self.engine:
                self.connect()
            metadata = MetaData()
            for table_name in table_names:
                if table_name not in self.tables:
                    metadata.reflect(bind=self.engine, only=[table_name], views=True, extend_existing=True)
                    self.tables[table_name] = metadata.tables[table_name]
        except Exception as e:
            self.logger.error(f"Error in initializing tables: {e}")
            raise Exception(f"Error in initializing tables: {e}")

    def initialize_tables2(self, tables_list):
        obj = {}
        for table in tables_list:
            obj[table] = model_mapping.get(table)
        self.tables = copy.deepcopy(obj)
        """Initialize tables based on the names provided."""
        # Dictionary mapping table names to classes

    def execute_query(self, query, dbname=None):
        """
        Executes a query on the specified database. Optionally switches databases if required.
        """

        session = None
        try:
            if dbname:
                self.switch_database(dbname)  # Switch the database if required
            if not self.engine:
                self.connect()

            session = self.Session()
            result = session.execute(query)

            # Check if the query is of type that requires a commit
            if hasattr(query, 'is_update') and (query.is_update or query.is_insert or query.is_delete):
                session.commit()

            # Fetch all results to avoid cursor issues
            return result  # Change here
        except Exception as e:
            if session:
                session.rollback()
            self.logger.error(f"Error in query execution: {e}")
            raise Exception(f"Error in query execution: {e}")

    def execute_query2(self, query, dbname=None, max_retries=3, retry_delay=5):
        """
        Executes a query on the specified database with a retry mechanism.
        Optionally switches databases if required.
        """
        attempt = 0
        session = None

        while attempt < max_retries:
            try:
                if dbname:
                    self.switch_database(dbname)  # Switch the database if required

                if not self.engine:
                    self.connect()

                session = self.Session()
                result = session.execute(query)

                # Check if the query is of a type that requires a commit
                if hasattr(query, 'is_update') and (query.is_update or query.is_insert or query.is_delete):
                    session.commit()

                # Fetch all results to avoid cursor issues and return them
                return result

            except (OperationalError, AttributeError) as e:
                # Rollback if an error occurs
                if session:
                    session.rollback()
                self.logger.error(f"Query Execution failed: {e}. Retrying {attempt + 1}/{max_retries}...")

                attempt += 1
                time.sleep(retry_delay)  # Delay before retrying

                # Reinitialize the connection if maximum attempts haven't been reached
                if attempt < max_retries:
                    self.engine.dispose()  # Close existing connections
                    self.connect()  # Reinitialize the connection and session
                else:
                    self.logger.error(f"Max retries reached. Query execution failed: {e}")
                    raise Exception(f"Error in query execution after {max_retries} attempts: {e}")

            except Exception as e:
                # Rollback and raise a general exception if it's not a transient error
                if session:
                    session.rollback()
                self.logger.error(f"Error in query execution: {e}")
                raise Exception(f"Error in query execution: {e}")


    def get_current_db(self):
        """
        Returns the name of the currently connected database.
        """
        return self.current_db
