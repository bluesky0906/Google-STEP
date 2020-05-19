#include <bits/stdc++.h>
#include <cctype>
using namespace std;

/*
    全通り順列 -> 辞書を二分探索
*/
string dic0_name ="class01/data/dictionary0.txt";
string dic_name ="class01/data/dictionary.txt";

bool my_next_permutation (string *s);
bool my_binary_search(string trg, vector<string> dic);
vector<string> read_dictionary();
void create_lower_dicrionary();

int main () {
    // ゲームでは大文字小文字区別しないので、小文字辞書を作る。
    // create_lower_dicrionary();

    string s;
    cin >> s;

    sort(s.begin(), s.end());

    // 順列生成
    vector<string> permutations;
    do {
        permutations.push_back(s);
    } while (my_next_permutation(&s));

    // 辞書
    vector<string> dic = read_dictionary();

    // 辞書を Binary search
    for (string per : permutations) {
        if (my_binary_search(per, dic)) {
            cout << "Anagram : " << per << endl;
        }
    }
    return 0;
}

// 順列生成 function
bool my_next_permutation (string *s) {
    int num = s->size();
    for (int i = num - 2; i >= 0; i--) {
        if (s->at(i) < s->at(i+1)) {
            for (int j = num - 1; j > i; j--) {
                if (s->at(i) < s->at(j)) {
                    swap(s->at(i), s->at(j));
                    reverse(s->begin()+(i+1), s->end());
                    return true;
                }
            }
        }
    }
    return false;
}

// 二分探索
bool my_binary_search(string trg, vector<string> dic) {
    auto left = dic.begin(), right = dic.end() - 1;

    while (right >= left) {
        auto mid = left + distance(left,right) / 2;
        if (*mid == trg) return true;
        else if (*mid > trg) right = mid - 1;
        else if (*mid < trg) left = mid + 1;
    }
    return false;
}

//　辞書の読み込み
vector<string> read_dictionary () {
    ifstream ifs(dic_name);
    string str;
    vector<string> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        dic.push_back(str);
    }
    return dic;
}

void create_lower_dicrionary() {
    ifstream ifs(dic0_name);
    string str;
    vector<string> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        // 大文字を小文字に直す
        transform(str.begin(), str.end(), str.begin(), [](unsigned char c){ return tolower(c); });
        dic.push_back(str);
    }

    // 大文字小文字変換したので辞書順に並べ直す
    sort(dic.begin(), dic.end());

    // 新しいファイルに書き込み
    ofstream outputfile(dic_name);
    for (auto d : dic) {
        outputfile << d << endl;
    }
    outputfile.close();
}