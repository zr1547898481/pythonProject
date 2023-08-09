# coding=utf-8
import yaml

def load_yaml():
    with open('../test_data/userData.yaml', 'r') as f :
        data = yaml.load(f,Loader=yaml.FullLoader)
        return data

if __name__ == '__main__':
    print(type(load_yaml()),load_yaml())