from db import MySQL


class Member(MySQL):
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM members WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
        return data

    def gets_by_year(self, year):
        if type(year) != int:
            raise TypeError
        query = 'SELECT * FROM members WHERE year = %s;'
        data = super.query(query, (year,))
        return data

    def gets_all(self):
        query = 'SELECT * FROM members;'
        data = super.query(query)
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
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM trainings WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
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
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM afters WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
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
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM restaurants WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
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
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM races WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
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
    def __init__(self):
        return super().__init__()

    def __del__(self):
        return super().__del__()

    def get_participants_by_id(self, id):
        raise NotImplementedError

    def get_by_id(self, id):
        if type(id) != int:
            raise TypeError
        query = 'SELECT * FROM results WHERE member_id = %s LIMIT 1;'
        data = super.query(query, (id,))
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
