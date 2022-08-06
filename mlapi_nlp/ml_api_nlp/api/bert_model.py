from torch import nn
from transformers import BertModel

model = BertModel.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking", output_attentions=False, output_hidden_states=False)

class BertForLivedoor(nn.Module):
    '''BERTモデルにLivedoorニュースの9クラスを判定する部分をつなげたモデル'''

    def __init__(self):
        super(BertForLivedoor, self).__init__()

        # BERTモジュール
        self.bert = model  # 日本語学習済みのBERTモデル

        # headにクラス予測を追加
        # 入力はBERTの出力特徴量の次元768、出力は9クラス
        self.cls = nn.Linear(in_features=768, out_features=9)

        # 重み初期化処理
        nn.init.normal_(self.cls.weight, std=0.02)
        nn.init.normal_(self.cls.bias, 0)

    def forward(self, input_ids):
        '''
        input_ids： [batch_size, sequence_length]の文章の単語IDの羅列
        '''

        # BERTの基本モデル部分の順伝搬
        # 順伝搬させる
        result = self.bert(input_ids)  # reult は、sequence_output, pooled_output

        # sequence_outputの先頭の単語ベクトルを抜き出す
        vec_0 = result[0]  # 最初の0がsequence_outputを示す
        vec_0 = vec_0[:, 0, :]  # 全バッチ。先頭0番目の単語の全768要素
        vec_0 = vec_0.view(-1, 768)  # sizeを[batch_size, hidden_size]に変換
        output = self.cls(vec_0)  # 全結合層

        return output