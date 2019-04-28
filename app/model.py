from db import MySQL


class Member(MySQL):
    def get_colnames(self):  # for test
        data = self.query('SHOW COLUMNS FROM members')
        return [col['Field'] for col in data]

    def get(self, id=None, year=None, limit=100):
        if type(id) == int:
            data = self.query('SELECT * FROM members WHERE member_id = %s LIMIT 1;', [id], dictionary=True)
        elif type(year) == int:
            data = self.query('SELECT * FROM members WHERE year = %s;', [year], dictionary=True)
        else:
            raise AttributeError
        return data

    def create(self, args):
        if not args.gets('family_name', False):
            raise LookupError
        if not args.gets('first_name', False):
            raise LookupError
        if not args.gets('kana', False):
            raise LookupError
        if not args.gets('show_name', False):
            raise LookupError
        if not args.gets('sex', False):
            raise LookupError
        if not args.gets('year', False):
            raise LookupError
        # visible = true when created

    def update(self, id, **args):
        if type(id) != int:
            raise TypeError
        if args.gets('family_name', False):
            pass
        if args.gets('first_name', False):
            pass
        if args.gets('kana', False):
            pass
        if args.gets('show_name', False):
            pass
        if args.gets('sex', False):
            pass
        if args.gets('year', False):
            pass
        if args.gets('visible', False):
            pass

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        if args.gets('family_name', False):
            pass
        if args.gets('first_name', False):
            pass
        if args.gets('kana', False):
            pass
        if args.gets('show_name', False):
            pass
        if args.gets('sex', False):
            pass
        if args.gets('year', False):
            pass
        if args.gets('visible', False):
            pass


class Training(MySQL):

    def get_participants_by_id(self, id):
        raise NotImplementedError


    def get(self, id=None, limit=1):
        if type(id) != int:
            data = self.query('SELECT * FROM trainings ORDER BY date DESC LIMIT %s;', (limit,), dictionary=True)
        else:
            data = self.query('SELECT * FROM trainings WHERE training_id = %s DESC LIMIT %s;', (id, limit,), dictionary=True)
        return data

    def create(self, args):
        raise NotImplementedError
        if not args.gets('family_name', False):
            raise LookupError

    def update(self, id, **args):
        raise NotImplementedError
        if type(id) != int:
            raise TypeError

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        # delete participants entries


class After(MySQL):
    def get_colnames(self):  # for test
        data = self.query('SHOW COLUMNS FROM afters', dictionary=True)
        return [col['Field'] for col in data]

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get(self, id=None, limit=1):
        if type(id) != int:
            data = self.query('SELECT * FROM afters ORDER BY date DESC , after_stage DESC  LIMIT %s;', (limit,), dictionary=True)
        else:
            data = self.query('SELECT * FROM afters WHERE after_id = %s DESC LIMIT %s;', (id, limit,), dictionary=True)
        return data

    def create(self, args):
        raise NotImplementedError
        if not args.gets('family_name', False):
            raise LookupError

    def update(self, id, **args):
        raise NotImplementedError
        if type(id) != int:
            raise TypeError

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        # delete participants entries


class Restaurant(MySQL):

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM restaurants WHERE member_id = %s LIMIT 1;'
        data = self.query(query, (id,))
        return data

    def create(self, args):
        raise NotImplementedError
        if not args.gets('family_name', False):
            raise LookupError

    def update(self, id, **args):
        raise NotImplementedError
        if type(id) != int:
            raise TypeError

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        # delete participants entries


class Race(MySQL):

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM races WHERE member_id = %s LIMIT 1;'
        data = self.query(query, (id,))
        return data

    def create(self, args):
        raise NotImplementedError
        if not args.gets('family_name', False):
            raise LookupError

    def update(self, id, **args):
        raise NotImplementedError
        if type(id) != int:
            raise TypeError

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        # delete participants entries


class Result(MySQL):

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM results WHERE member_id = %s LIMIT 1;'
        data = self.query(query, (id,))
        return data

    def create(self, args):
        raise NotImplementedError
        if not args.gets('family_name', False):
            raise LookupError

    def update(self, id, **args):
        raise NotImplementedError
        if type(id) != int:
            raise TypeError

    def delete(self, id, **args):
        if type(id) != int:
            raise TypeError
        # delete participants entries
