import os
import pandas as pd


def main():
    db = {
        'username': [],
        'password': [],
        'model_parameters': [],
    }

    pd_db = pd.DataFrame.from_dict(db)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'local_tmp'))
    if not os.path.exists(path):
        os.makedirs(path)

    pd.to_pickle(pd_db, os.path.join(path, 'db.pickle'))


if __name__ == '__main__':
    main()
