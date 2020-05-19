#include <bits/stdc++.h>
using namespace std;

/*
    ソートされた辞書を使う
*/
string dic_name ="class01/data/dictionary.txt";
string sorted_dic_name = "class01/data/sorted_dictionary.txt";

void create_sorted_dictionary();
map<string, vector<string>> read_sorted_dictionary();

int main () {
    // 新しい辞書を作る
    // create_sorted_dictionary();

    // 入力文字列
    string s;
    cin >> s;
    sort(s.begin(), s.end());

    // 辞書読み込み
    map<string, vector<string>> dic = read_sorted_dictionary();

    // mapにアクセス
    for (string anagram : dic[s]) {
        cout << "Anagram: " << anagram << endl;
    }
}

//　辞書の読み込み
void create_sorted_dictionary () {
    ifstream ifs(dic_name);
    string str;

    map<string,string> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        // 各文字列をsortして、新しい辞書を作る
        // key:ソート済文字列, value:ソート前文字列1 ソート前文字列2 ...
        string tmp = str;
        sort(str.begin(), str.end());

        if ((dic.find(str)) == dic.end()) {
            dic[str] = tmp;
        }
        else {
            dic[str]+= " " + tmp;
        }
    }

    // 新しいファイルに書き込み
    // ソートされた文字列 ソート前文字列1 ソート前文字列2 ...
    ofstream outputfile(sorted_dic_name);
    for (auto d : dic) {
        outputfile << d.first << " " << d.second << endl;
    }
    outputfile.close();
}

//　ソートされた辞書の読み込み
map<string, vector<string>> read_sorted_dictionary() {
    // key:ソート済文字列, value:ソート前文字列1 ソート前文字列2 ...
    ifstream ifs(sorted_dic_name);
    string str;
    map<string, vector<string>> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        stringstream ss;
        ss << str;

        string key, s;
        vector<string> val;
        ss >> key;
        while(getline(ss, s, ' ')) {
            ss >> s;
            val.push_back(s);
        }
         
        dic[key] = val;
    }
    return dic;
}