import re

### 正規表現
# 文頭が[key:C#]みたいな形
keyRegex = r'^\[(K|k)ey\s?:\s?[A-G](#|b|)\] '
# ルート音だけ拾うやつ
rootRegex = r'[A-G](#|b|)'

def getKey(txt: str):
    # テキストからキーを取得
    keyData = re.search(keyRegex, txt)
    if keyData == None: return

    key = re.search(rootRegex, keyData.group())
    if keyData != None:
        return key.group()
    

def removeKeyData(txt: str):
    # キーの情報を削除して返す
    return re.sub(keyRegex, '', txt)


def getChords(txt: str):
    # テキストからコードを取得
    # 空白を削除
    txt = txt.replace(' ', '')
    chords = txt.split('-')

    return chords


def getDegree(note : str):
    '''ルート音のディグリーを返す
    note: 一文字のみ
    '''
    # 範囲外はパス
    if not re.match(rootRegex, note): return

    degreeDict = {
        'C': 0,
        'D': 1,
        'E': 2,
        'F': 2.5,
        'G': 3.5,
        'A': 4.5,
        'B': 5.5,
    }

    # ルート（符号なし）のディグリーを抽出
    root = re.sub(r'#|b', '', note)

    # 符号の誤差
    fugo = note.replace(root, '')
    r = {'#': 0.5, 'b': -0.5, '': 0}[fugo]

    if root in degreeDict:
        return degreeDict[root] + r


def getDegreeName(deg: float, lastChord: str):
    '''ディグリーネームを取得する
    lastChordは符号の対応に使用
    '''
    lastChord = getDegree(lastChord)

    degreeDict = {
        0: 'Ⅰ',
        1: 'Ⅱ',
        2: 'Ⅲ',
        2.5: 'Ⅳ',
        3.5: 'Ⅴ',
        4.5: 'Ⅵ',
        5.5: 'Ⅶ',
    }

    # 符号なし
    if deg in degreeDict:
        return degreeDict[deg]
    
    # 符号あり
    else:
        # 一つ前のコードと高低差を比較して符号をつける
        # 空白の場合
        if lastChord == '':
            return 'b' + degreeDict[deg + 0.5]
        # bⅦは例外処理
        if deg == 5.0:
            return 'b' + degreeDict[deg + 0.5]
        
        if lastChord < deg:
            return '#' + degreeDict[deg - 0.5]
        else:
            return 'b' + degreeDict[deg + 0.5]


def convertChords(data : str, key : str):
    '''コードネームからディグリーネームに書き換える
    '''

    diff = getDegree(key)
    chords = getChords(data)

    # ルート音を集めたリスト
    rootList = [re.findall(r'([A-G](#|b|))', c) for c in chords]
    # ディグリーに変換したリスト
    degList = []
    for i, root in enumerate(rootList):
        l = []
        for r in root:
            root = r[0]
            deg = (getDegree(root) - diff)
            l.append(getDegreeName(deg % 6.0, rootList[i-1][0][0]))
        
        degList.append(l)

    # 整形
    rootList = [r[0] for r in rootList[0]]
    # 辞書を作成
    convertDict = dict(zip(rootList, degList[0]))
    # 辞書に従って変換して返す
    convertRegex = '({})'.format('|'.join(map(re.escape, convertDict.keys())))
    return re.sub(convertRegex, lambda m: convertDict[m.group()], data)


def isInvalid(txt: str):
    # 入力が正しいか判断する
    a = getChords(txt)
    b = re.sub(keyRegex, '', txt)
    b = re.findall(r'([A-G](#|b|))', txt)
    slash = re.findall(r'/', txt)
    return len(a) != len(b) - 1 - len(slash)


def convert2Degree(input: str):
    '''一連の流れをまとめたもの
    '''
    result = convertChords(removeKeyData(input), getKey(input))
    return ''.join(result)