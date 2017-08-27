#encoding=utf-8
import sys
sys.path.append("../")
import jieba
import csv
jieba.load_userdict('mydict.txt')


def cuttest(test_sent):
    result = jieba.cut(test_sent)
    print(", ".join(result))


def get_content():
    with open('../data_cleaned_2.csv', 'r') as f:
    # with open('data_part.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        # print(f_csv)

        line_num = 0
        for row in f_csv:
            # print(row[6].strip())
            if line_num < 100:
                cuttest(row[6].strip())
                line_num += 1
            else:
                break



if __name__ == "__main__":
   get_content()