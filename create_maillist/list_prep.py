import pandas as pd
# from clevercsv import read_dataframe


def open_df(path:str) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8", delimiter=";")


def save_df(df:pd.DataFrame, path:str) -> None:
    df = df.sample(frac = 1)
    df.to_csv(path, encoding="utf-8", sep = ";", header=True, index=False)


def delete_empty(df:pd.DataFrame) -> pd.DataFrame:
    print(f"Deleted: {len(df[df['email'].isnull()])} rows")
    return df[df["email"].notnull()]


def delete_email_copies(df:pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset=['email'])


def delete_rg(df:pd.DataFrame) -> pd.DataFrame:
    print("Deleting this rows:")
    print(df[df["email"].str.contains("rg.ru")])
    print(df[df["email"].str.contains("2gis.ru")])
    print(df[df["name"].str.contains("Российская газета")])
    df = df[~df["email"].str.contains("rg.ru")]
    df = df[~df["email"].str.contains("2gis.ru")]
    df = df[~df["name"].str.contains("Российская газета")]
    return df


def delete_keyword(df:pd.DataFrame, keyword:str) -> pd.DataFrame:
    print(df[df["name"].str.contains(keyword, case=False)])
    df = df[~df["name"].str.contains(keyword, case=False)]
    return df


def manual_delete(df:pd.DataFrame) -> pd.DataFrame:
    for i, row in df.iterrows():
        print(f"\nRow number: {i}\n{row}")
        del_row = input("Press 1 if you want to delete this row!\
                        \nPress 2 to save changes in dataframe.\n")
        if del_row == '1':
            df.drop(df.index[i], inplace=True)
            print(f"Row number {i} deleted!")
        elif del_row == '2':
            print("Saving changes in dataframe....")
            return df
    return df


def add_commas(df:pd.DataFrame) -> pd.DataFrame:
    df['email'] = df['email'].str.replace(' ',', ')
    return df


def create_email_df(df:pd.DataFrame) -> pd.DataFrame:
    df['email'] = df['email'].str.replace(',',' ')
    emails = set()
    for row in df['email']:
        for email in row.split():
            emails.add(email)
    df = pd.DataFrame(emails)
    print(df)
    
    return df


def print_df(df:pd.DataFrame) -> None:
    print(df)
    print(df.info())
    print(df.describe())
    print(df.columns)


def main():
    DF_PATH = "D:/OneDrive/data/2gis/news/gazety_ia.csv"
    KW_LIST =['ремонт','наук', 'науч', 'авто', 'строй', 'бухг', 'детск', 
              'работ', 'недвиж', 'охот', 'хими', 'студ', 'физи', 'кроссв',
              'тв-програм', 'спорт', 'медиц', 'здоров', 'труд', 'цены', 
              'апте', 'ярмар', 'объявлен', 'прода', 'реклам', 'знаком', 
              'строит','дачн', 'avto', 'auto', 'аренд', 'налог', 'курорт', 
              'бирж', 'закон', 'футбол', 'воен', 'сельск', 'православн',
              'промышлен', 'аэро', 'все для вас', 'мода', 'женск', 'квартир', 
              'UUUUUU', 'UUUUU', 'UUUUUU', 'UUUUU', 'UUUUUU', 'UUUUU', 
              'UUUUUU', 'UUUUU'] # 'мото', 
    df = open_df(DF_PATH)
    # df = delete_empty(df)
    # df = delete_rg(df)
    # df = delete_email_copies(df)
    # for kw in KW_LIST:
    #     df = delete_keyword(df, kw)
    # df = add_commas(df)
    df = create_email_df(df)
    save_df(df, "D:/OneDrive/data/2gis/news/gazety_ia_emails.csv")


    # print(df)
    # save_df(df, DF_PATH)
    # print_df(df)


if __name__ == "__main__":
    main()