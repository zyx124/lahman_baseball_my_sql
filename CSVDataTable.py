import csv
import copy
import json
import logging

class Index():

    def __init__(self, name=None, table=None, columns=None, kind=None, loadit=None):
        self.name = name
        self.table = table
        self.columns = columns
        self.kind = kind
        self._index_data = None

    def compute_key(self, row):

        key_v = [row[k] for k in self.columns]
        key_v = "_".join(key_v)
        return key_v

    def add_to_index(self, row, rid):

        if self._index_data is None:
            self._index_data = {}

        key = self.compute_key(row)
        bucket = self._index_data.get(key, [])
        if self.kind != 'INDEX':
            if len(bucket) > 0:
                raise KeyError('Duplicate Key')

        bucket.append(rid)
        self._index_data[key] = bucket

    def get_no_of_entrys(self):
        return len(self.columns)

    def matches_index(self, tmp):

        k = set(list(tmp.keys()))
        c = set(self.columns)
        # Index matches. Return the number of indexes.
        if c.issubset(k):
            if self._index_data is not None:
                kk = len(self._index_data.keys())
            else:
                kk = 0
        else:
            kk = None

        return kk

    def to_json(self):

        r = {}
        r['name'] = self.name
        r['columns'] = self.columns
        r['kind'] = self.kind
        r['table_name'] = self.table
        r['index_data'] = self._index_data

        return r

    def find_rows(self, tmp):
        t_vals = [tmp[k] for k in self.columns]
        t_s = '_'.join(t_vals)

        d = self._index_data.get(t_s, None)
        # if d is not None:
        #     d = list(d.keys())

        return d







class CSVDataTable():

    def __init__(self, table_name, connect_info=None, column_names=None,primary_key_columns=None, loadit=False):

        self._table_name = table_name
        self._connect_info = connect_info
        self._key_columns = primary_key_columns

        self._indexes = None

        self._column_names = None
        self._default_directory = '/home/zyx/database_hw/Yuxin_Zhao_yz3400_HW3/DB/'
        self._rows = None
        self._next_row_id = 0
        if not loadit:
            if column_names is None or table_name is None:
                raise ValueError('Please provide table name or column names')

            self._next_row_id = 1

            self._rows = {}

            if primary_key_columns:
                self.add_index('PRIMARY', self._key_columns, 'PRIMARY')




    # def __str__(self):
    #     # return information about the table and the first rows for preview.
    #     result = str(type(self)) + ': name = ' + self._table_name
    #     result += '\n connect_info = ' + str(self._connect_info)
    #     result += '\n Key columns = ' + str(self._key_columns)
    #     if self._column_names is not None:
    #         result += '\n Column Names = ' + str(self._column_names)
    #     if self._rows is not None:
    #         row_count = len(self._rows)
    #     else:
    #         row_count = 0
    #     result += '\n No. of rows = ' + str(row_count)
    #
    #     to_print = min(5, row_count)
    #     for i in range(to_print):
    #         result += '\n' + str(self._rows[i])
    #     return result
    def get_rows(self):
        rows = []
        for k, v in self._rows.items():
            rows.append(v)

        return rows

    def load_csv(self):
        fn = self._connect_info['directory'] + '/' + self._connect_info['file_name']
        with open(fn, 'r') as input_rows:
            c_reader = csv.DictReader(input_rows)
            for r in c_reader:
                if self._column_names is None:
                    self._column_names = list(r.keys())
                if self._rows is None:
                    self._rows = []

                self._add_row(r)

    def load(self, directory):
        # The function is to load json files which contains info of a table
        if '.json' not in directory:
            file = directory + self._table_name + '.json'
        else:
            file = directory

        with open(file, "r") as f:
            d = json.load(f)

            state = d['state']
            self._table_name = state['table_name']
            self._key_columns = state['primary_key_columns']
            self._column_names = state['column_names']
            self._rows = d['rows']

        for k,v in d['indexes'].items():
            idx = Index(loadit=v, table=self)
            if self._indexes is None:
                self._indexes = {}
            self._indexes[k] = idx

    def get_best_index(self, t):
        """

        :param t: template
        :return: best index
        """
        best = None
        n = None

        if self._indexes is not None:
            for k,v in self._indexes.items():
                cnt = v.matches_index(t)

                if cnt is not None:
                    if best is None:
                        best = cnt
                        n = k
                    else:
                        if cnt>best:
                            best = len(v.keys())
                            n = k

        return n

    def find_by_index(self, tmp, idx):
        r = idx.find_rows(tmp)
        res = [self._rows[k] for k in r]
        return res

    def _project(self, rows, field_list):

        if field_list is None:
            return rows
        if not rows:
            return None
        new_rows = []
        for r in rows:
            new_r = {f: r[f] for f in field_list}
            new_rows.append(new_r)
        return new_rows

    def find_by_scan_template(self, tmp, res, field_list):
        some_rows = None
        for r in res:
            if self.matches_template(tmp, r):
                if some_rows is None:
                    some_rows = []
                some_rows.append(copy.copy(r))

        r = self._project(some_rows, field_list)
        return r

    def find_by_template(self, tmp, field_list=None, use_index=True):

        if tmp is None:
            new_t = CSVDataTable(table_name='Derived:' + self._table_name, loadit=True)
            new_t.import_data(self.get_rows())
            return new_t

        idx = self.get_best_index(tmp)
        logging.debug('Using  index = %s', idx)

        if idx is None or use_index==False:

            result = self.find_by_scan_template(tmp, self.get_rows(), field_list)
        else:
            idx = self._indexes[idx]
            res = self.find_by_index(tmp, idx)
            result = self.find_by_scan_template(tmp, res, field_list)

        if result:
            new_t = CSVDataTable(table_name='Derived:' + self._table_name, loadit=True)
            new_t.import_data(result)

            return new_t
        else:

            return None

    # def load_from_rows(self, table_name, rows):


    def matches_template(self, tmp, row):

        if tmp is None:
            return True

        keys = tmp.keys()
        for k in keys:
            v = row.get(k, None)
            if tmp[k] != v:
                return False

        return True

    def _get_key(self, row):
        result = [row[k] for k in self._key_columns]
        return result

    def add_index(self, name, columns, kind):

        if self._indexes is None:
            self._indexes = {}

        self._indexes[name] = Index(name=name, columns=columns, kind=kind)
        self.build(name)

    def build(self, i_name):

        idx = self._indexes[i_name]
        for k,v in self._rows.items():
            idx.add_to_index(v,k)


    def get_next_row_id(self):
        self._next_row_id += 1
        return self._next_row_id

    def import_data(self, rows):
        for r in rows:
            self.insert(r)

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records. Raises an exception if this
            creates a duplicate primary key.
        :return: None
        """
        if self._rows is None:
            self._rows = {}
        rid = self.get_next_row_id()
        self._rows[rid] = copy.copy(new_record)

        if self._indexes is not None:
            for n, idx in self._indexes.items():
                idx.add_to_index(new_record, rid)

    def get_index_and_selectivity(self, on_c):
        """

        :param on_c: on clause
        :return: the best index and number of rows that can be selected.
        """
        on_tmp = dict(zip(on_c,  [None]*len(on_c)))
        best = None
        n = self.get_best_index(on_tmp)
        if n is not None:
            best = len(list(self._rows.keys()))/(self._indexes[n].get_no_of_entrys())

        return n, best

    def _get_specific_where(self, wc):

        result = {}
        if wc is not None:
            for k,v in wc.items():
                kk = k.split('.')
                if len(kk) == 1:
                    result[k] = v
                elif kk[0] == self._table_name:
                    result[kk[1]] = v

        if result =={}:
            result = None

        return result

    def _get_specific_project(self, p_clause):

        result = []
        if p_clause is not None:
            for k in p_clause:
                kk = k.split('.')
                if len(kk) == 1:
                    result.append(k)
                elif kk[0] == self._table_name:
                    result.append(kk[1])
        if result == []:
            result = None

        return result

    @staticmethod
    def on_clause_to_where(on_c, r):

        result = {c:r[c] for c in on_c}
        return result


    @staticmethod
    def _get_scan_probe(l_table, r_table, on_clause):

        s_best, s_selective = l_table.get_index_and_selectivity(on_clause)
        r_best, r_selective = r_table.get_index_and_selectivity(on_clause)

        result = l_table, r_table

        if s_best is None and r_best is None:
            result = l_table, r_table
        elif s_best is None and r_best is not None:
            result = r_table, l_table
        elif s_best is not None and r_best is None:
            result = l_table, r_table
        elif s_best is not None and r_best is not None and s_selective<r_selective:
            result = r_table, l_table

        return result

    def join(self, right_t, on_clause, w_clause=None, p_clause=None, optimize = True):
        s_table, p_table = self._get_scan_probe(self, right_t, on_clause)

        if s_table != self and optimize:
            logging.debug('Swapping tables')

        if optimize:
            s_tmp = s_table._get_specific_where(w_clause)
            s_proj = s_table._get_specific_project(p_clause)

            s_rows = s_table.find_by_template(s_tmp, s_proj)
        else:
            s_rows = s_table

        if s_rows is None:
            logging.debug('Find Nothing!')
            return
        scan_rows = s_rows.get_rows()

        result = []

        for r in scan_rows:
            p_where = CSVDataTable.on_clause_to_where(on_clause, r)
            p_project = p_table._get_specific_project(p_clause)

            p_rows = p_table.find_by_template(p_where, p_project)
            if p_rows is not None:
                p_rows = p_rows.get_rows()

            if p_rows:
                for i in p_rows:
                    new_r = {**r, **i}
                    result.append(new_r)
        tn = "Join(" + self._table_name+','+right_t._table_name+')'
        final_result = CSVDataTable(table_name=tn, loadit=True)

        final_result.import_data(result)

        return final_result




    def _add_row(self, r):
        if self._rows is None:
            self._rows = []
        k = self._get_key(r)
        test_it = self.find_by_primary_key(k)
        if test_it is not None:
            raise ValueError('what part of unique is not clear')
        else:
            self._rows.append(r)

    def delete_by_template(self, template):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        new_rows = []
        count = 0
        for n, r in self._rows.items():
            if not self.matches_template(template, r):
                new_rows.append(copy.copy(r))
            else:
                count = count + 1
        self._rows = new_rows

        return count

    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """
        tmp = dict(zip(self._key_columns, key_fields))
        result = self.find_by_template(tmp, field_list)
        rows = result.get_rows()
        if rows and len(rows) > 0:
            return rows[0]
        else:
            return None

    def _update_row(self, r, new_values):
        keys = new_values.keys()
        new_r = copy.copy(r)
        for k in keys:
            new_r[k] = new_values[k]
        return new_r

    def update_by_template(self, template, new_values):
        """

        :param template: A template that defines which matching rows to update.
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """

        count = 0
        for r in self._rows:
            if self.matches_template(template, r):

                count += 1
                new_r = self._update_row(r, new_values)
                new_k = self._get_key(new_r)
                self._rows.remove(r)
                k = self.find_by_primary_key(new_k)

                if k is not None:
                    self._add_row(r)
                    raise ValueError('ick')
                else:
                    self._add_row(new_r)

        return count

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of values for primary key fields
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """
        tmp = dict(zip(self._key_columns, key_fields))
        result = self.update_by_template(tmp, new_values)
        return result

    def save(self):

        d = {
            'state':{
                'table_name': self._table_name,
                'primary_key_columns': self._key_columns,
                'next_rid': self.get_next_row_id(),
                'column_names': self._column_names
            }
        }

        fn = self._default_directory + self._table_name + '.json'
        d['rows'] = self._rows

        for k,v in self._indexes.items():
            idxs = d.get('indexes', {})
            idx_string = v.to_json()
            idxs[k] = idx_string
            d['indexes'] = idxs

        d = json.dumps(d, indent=2)
        with open(fn, 'w+') as outfile:
            outfile.write(d)
