#include <bits/stdc++.h>

using namespace std;

/*
    ランレングス圧縮をした辞書を使う
*/

string dic_name ="class01/data/dictionary.txt";
string encorded_dic_name = "class01/data/encorded_dictionary.txt";

void create_encorded_dictionary();
void run_length(string &s);
map<string, vector<string>> read_encorded_dictionary();
bool length_comp(string a, string b);

int main () {
    // 新しい辞書を作る
    create_encorded_dictionary();

    // 辞書読み込み
    map<string, vector<string>> dic = read_encorded_dictionary();
    
    // 入力された文字列
    string s;
    cin >> s;
    run_length(s);

    // key: sに含まれる文字, value: sの回数
    map<char,int> s_map;
    for (int i=0; i<s.size()-1; i++) {
        if (i % 2 == 1) continue;
        s_map[s.at(i)] = atoi(&s.at(i+1));
    }

    vector<string> anagrams;

    // 辞書と比較
    for (auto d : dic) {
        string key = d.first;

        // anagramになっている時与えられた文字の方が短いことはない(文字の種類が多いわけはない)
        if (s.size() < key.size()) continue;


        bool isAna = true;
        
        // 各文字を比較
        for (int i=0; i<key.size()-1; i++) {
            if (i % 2 == 1) continue;
            // 文字が使われている回数が辞書よりも少なかったらダメ
            if (s_map[key.at(i)] < atoi(&key.at(i+1))) {
                isAna = false;
                break;
            }
        }
        // 全ての文字に対してオッケーだったらanagram
        if (isAna) {
            for (string v : d.second) {
                anagrams.push_back(v);
            }
        }

    }
    // 長さsort
    sort(anagrams.begin(), anagrams.end(), length_comp);

    for (string ana : anagrams) {
        cout << ana << endl;
    }
}

void run_length(string &s) {
    string t = "";
    int count = 1;
    char tmp = s.at(0);
    for (int i=1; i<s.size(); i++) {
        if (tmp == s.at(i)) {
            count++;
        }
        else {
            t += tmp + to_string(count);
            tmp = s.at(i);
            count = 1;
        }
    }
    t += tmp + to_string(count);

    s = t;
}

// 長さ比較
bool length_comp(string a, string b) {
    return a.size() > b.size();
}

void create_encorded_dictionary() {
    ifstream ifs(dic_name);
    string str;

    map<string,string> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        // 各文字列をsortして、新しい辞書を作る
        // key:エンコード済文字列, value:エンコード前文字列1 エンコード前文字列2 ...
        string tmp = str;
        sort(str.begin(), str.end());
        run_length(str);

        if ((dic.find(str)) == dic.end()) {
            dic[str] = tmp;
        }
        else {
            dic[str]+= " " + tmp;
        }
    }

    // 新しいファイルに書き込み
    // エンコードされた文字列 エンコード前文字列1 エンコード前文字列2 ...
    ofstream outputfile(encorded_dic_name);
    for (auto d : dic) {
        outputfile << d.first << " " << d.second << endl;
    }
    outputfile.close();
}

//　エンコードされた辞書の読み込み
map<string, vector<string>> read_encorded_dictionary() {
    // key:エンコード済文字列, value:エンコード前文字列1 エンコード前文字列2 ...
    ifstream ifs(encorded_dic_name);
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