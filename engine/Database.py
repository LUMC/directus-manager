from sqlalchemy import create_engine


class db:
    def __init__(self, username, password, database=None):
        self.dialect = 'mysql'
        self.driver = 'pymysql'
        self.host = 'localhost'
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        engine = create_engine('{dialect}+{driver}://{user}:{password}@{host}'.format(
            dialect=self.dialect,
            driver=self.driver,
            user=self.username,
            password=self.password,
            host=self.host
        ))
        try:
            connection = engine.connect()
            self.connection = connection
            return True
        except Exception as error:
            print("\nDatabase connection failed\nTry again...\n")
            return False

    def connect_to_db(self, name):
        engine = create_engine('{dialect}+{driver}://{user}:{password}@{host}/{database}'.format(
            dialect=self.dialect,
            driver=self.driver,
            user=self.username,
            password=self.password,
            host=self.host,
            database=name
        ))
        try:
            connection = engine.connect()
            self.connection = connection
            return True
        except Exception as error:
            print("\nDatabase connection failed\nTry again...\n")
            return False

    def add_db(self, name):
        self.connect()
        self.connection.execute('CREATE DATABASE {name}'.format(name=name))
        self.connection.close()

    def drop_db(self, name):
        self.connect()
        self.connection.execute('DROP DATABASE {name}'.format(name=name))
        self.connection.close()

    def check_name_unique(self, name):
        existing_databases = self.connection.execute("SHOW DATABASES;")
        return True if name in [d[0] for d in existing_databases] else False

    def get_db_databases(self):
        self.connect()
        result = self.connection.execute('SHOW databases;')
        self.connection.close()
        return [item for item in result]

    def get_db_tables(self):
        if self.database:
            self.connect()
            result =  self.connection.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = '{name}';".format(name=self.database)
            )
            self.connection.close()
            return [item for item in result]