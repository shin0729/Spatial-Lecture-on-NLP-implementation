import os
from dotenv import load_dotenv
import re
import preprocess
# .envファイルの内容を読み込見込む
if __name__ == "__main__":
    load_dotenv()
    
    # os.environを用いて環境変数を変数に格納する
    #データセットへのpathを各自envファイルに設定する
    atheism_path = os.environ["FILEPATH_ATHEUSM"]
    christian_path = os.environ["FILEPATH_CHRISTIAN"]
    test_atheism_path = os.environ["FILEPATH_TEST_ATHEUSM"]
    test_christian_path = os.environ["FILEPATH_TEST_CHRISTIAN"]
    # ファイルの中にある文章を読み込む
    # すべてのファイルに対して「lines:」以降の文章を取得する
    contents_atheusm = preprocess.preprocess_text(atheism_path)
    contents_christian = preprocess.preprocess_text(christian_path)
    contents_test_atheusm = preprocess.preprocess_text(test_atheism_path)
    contents_test_christian = preprocess.preprocess_text(test_christian_path)