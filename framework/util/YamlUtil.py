# -*- coding: utf-8 -*-
# @Time    : 2022/3/12 15:44
# @Author  : zjz

import yaml


from config.pytest_config import Const


def save_yaml(file, yml_data):
    with open(file, 'w', encoding='utf-8') as outfile:
        yaml.dump(yml_data, outfile, allow_unicode=True, width=1000)


def find_dic_data(key, data):
    try:
        if isinstance(data, dict):
            if key in data:
                return data[key]
            else:
                for item, value in data.items():
                    result = find_dic_data(key, value)
                    if result is not None:
                        return result
        else:
            return None
    except:
        return None


#
# def get_yml_file_path(file):
#     parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#     yml_file = os.path.join(parent_path, 'testscript', 'PageMapping', file)
#     return yml_file


def load_yml(yml_file):
    with open(yml_file, 'r', encoding='utf-8') as f:
        r = f.read()
    data = yaml.load(r, Loader=yaml.FullLoader)
    return data


class ColorYml:

    def __init__(self, file=None):
        if file:
            self.data = load_yml(file)
        else:
            self.data = load_yml(Const.RESOURCE_COLOR_FILE)

    def get_color(self, key):
        return find_dic_data(key, self.data)


class CaseYml:

    def __init__(self, file_name):
        self.file_path = file_name
        self.root_path = file_name.replace(file_name.split('/')[-1], '')

        # self.data_paraphrase(self.data, self.import_data)

    def get_import_data(self):
        import_data = dict()
        data = load_yml(self.file_path)
        import_yml = ''
        if 'import' in data:
            import_yml = data.pop('import')
        if isinstance(import_yml, str):
            import_yml_list = import_yml.split(',')
            for one_yml in import_yml_list:
                if one_yml:
                    import_yml_path = one_yml.strip()
                    import_data.update(load_yml(self.root_path + import_yml_path))
        elif isinstance(import_yml, list):
            for one_yml in import_yml:
                if one_yml:
                    import_yml_path = one_yml.strip()
                    import_data.update(load_yml(import_yml_path))
        return data, import_data

    # def find_all_test_actions(self,key, import_value, data):
    #     result = []
    #     if 'test_step' in data:
    #         test_actions = data['test_step']
    #         if isinstance(test_actions, list):
    #             for item in test_actions:
    #                 if isinstance(item, dict):
    #                     if key == item.keys()[0]:
    #                         import_value.update(item[key])
    #                         test_actions[key]


if __name__ == '__main__':
    yml_instance = CaseYml('ep1.0/test_message_center.yml')
    _data = yml_instance.data
    print(_data)
