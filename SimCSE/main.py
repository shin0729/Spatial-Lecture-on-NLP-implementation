import os
import sys
print(sys.path)
from dotenv import load_dotenv
import re
import preprocess
import embedding
import numpy as np
from sklearn.svm import SVC
import torch
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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

    embeds_atheusm = embedding.embed_text_SimSCE(contents_atheusm)
    embeds_christian = embedding.embed_text_SimSCE(contents_christian)
    embeds_test_atheusm = embedding.embed_text_SimSCE(contents_test_atheusm)
    embeds_test_christian = embedding.embed_text_SimSCE(contents_test_christian)

    embeds_atheusm_np = np.array([tensor.detach().cpu().numpy() for tensor in embeds_atheusm])
    embeds_christian_np = np.array([tensor.detach().cpu().numpy() for tensor in embeds_christian])
    embeds_test_atheusm_np = np.array([tensor.detach().cpu().numpy() for tensor in embeds_test_atheusm])
    embeds_test_christian_np = np.array([tensor.detach().cpu().numpy() for tensor in embeds_test_christian])

    print("Shape of embeds_atheusm_np:", embeds_atheusm_np.shape)
    # print("Type of embeds_atheusm:", type(embeds_atheusm))
    # print("Length of embeds_atheusm:", len(embeds_atheusm))
    # if len(embeds_atheusm) > 0:
    #     print("Type of first element:", type(embeds_atheusm[0]))
    #     if hasattr(embeds_atheusm[0], 'shape'):
    #         print("Shape of first element:", embeds_atheusm[0].shape)
    all_embeds = np.concatenate([embeds_atheusm_np, embeds_christian_np])

    # 結果の形状を確認
    print("Shape of all_embeds:", all_embeds.shape)
    #学習データの作成
    labels = np.array([0]*len(embeds_atheusm_np) + [1]*len(embeds_christian_np))
    #埋込を結合
    # all_embeds = np.concatenate([embeds_atheusm, embeds_christian])
    #分類器の学習
    classifier = SVC()
    classifier.fit(all_embeds, labels)

    #テストデータで評価
    
    anthesum_count = 0
    for i, embed in enumerate(embeds_test_atheusm_np):
        pred = classifier.predict([embed])
        if pred == 0:
            anthesum_count += 1

    christian_count = 0
    for i, embed in enumerate(embeds_test_christian_np):
        pred = classifier.predict([embed])
        if pred == 1:
            christian_count += 1
    print("number of train data:", str(len(embeds_atheusm)) +","+ str(len(embeds_christian)))
    print("number of test data:", str(len(embeds_test_atheusm)) +","+ str(len(embeds_test_christian)))
    print("christian acc:", str(christian_count / len(embeds_test_christian)))
    print("atheusm acc:", str(anthesum_count / len(embeds_test_atheusm)))



    # 主成分分析で2次元に削減
    pca = PCA(n_components=2)
    all_embeds_2d = pca.fit_transform(all_embeds)
    test_embeds_2d = pca.transform(np.concatenate([embeds_test_atheusm_np, embeds_test_christian_np]))

    # 訓練データとテストデータの可視化
    plt.figure(figsize=(12, 8))
    plt.scatter(all_embeds_2d[labels==0, 0], all_embeds_2d[labels==0, 1], color='red', marker='o', label='Atheism (Train)')
    plt.scatter(all_embeds_2d[labels==1, 0], all_embeds_2d[labels==1, 1], color='blue', marker='s', label='Christian (Train)')
    plt.scatter(test_embeds_2d[:len(embeds_test_atheusm_np), 0], test_embeds_2d[:len(embeds_test_atheusm_np), 1], color='lightcoral', marker='^', label='Atheism (Test)')
    plt.scatter(test_embeds_2d[len(embeds_test_atheusm_np):, 0], test_embeds_2d[len(embeds_test_atheusm_np):, 1], color='lightblue', marker='v', label='Christian (Test)')

    # 決定境界の可視化
    x_min, x_max = all_embeds_2d[:, 0].min() - 1, all_embeds_2d[:, 0].max() + 1
    y_min, y_max = all_embeds_2d[:, 1].min() - 1, all_embeds_2d[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, (x_max - x_min) / 100),
                        np.arange(y_min, y_max, (y_max - y_min) / 100))
    Z = classifier.decision_function(pca.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])

    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.title('SVM Decision Boundary (PCA)')
    plt.legend()
    plt.show()
