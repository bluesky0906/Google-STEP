#include <bits/stdc++.h>
using namespace std;

/*
    ソートされた辞書を使う
*/
string sorted_dic_name = "class01/data/sorted_dictionary.txt";


bool comp(pair<string, int> a, pair<string, int> b);
bool length_comp(string a, string b);
map<string, vector<string>> read_sorted_dictionary();
vector<pair<string, int>> calculate_scores (set<string> anagrams);
void find_qu(set<string> anagrams);

int main () {

    // 辞書読み込み
    map<string, vector<string>> dic = read_sorted_dictionary();
    
    // 入力文字列
    string s;
    cin >> s;
    sort(s.begin(), s.end());

    vector<string> candidates = {""};
    set<string> anagrams;

    for (char c : s) {
        vector<string> current_candidates = candidates;
        for (string prev : current_candidates) {
            string new_candidate = prev + c;
            if (dic.find(new_candidate) != dic.end()) {
                for (string v : dic[new_candidate]) {
                    anagrams.insert(v);
                }
            }
            candidates.push_back(new_candidate);
        }
    }


    vector<pair<string, int>> calculated_anagrams;
    calculated_anagrams = calculate_scores(anagrams);
    

    // 点数順 ->　長さソート
    sort(calculated_anagrams.begin(), calculated_anagrams.end(), comp);
    
    for (int i=0; i<10; i++) {
        if (calculated_anagrams.size() < i) break;
        cout << i << ": " << calculated_anagrams.at(i).first << endl;
    }
}

map<char,int> letters_score {
    make_pair('a', 1), make_pair('b', 1), make_pair('c', 2), make_pair('d', 1), make_pair('e', 1),
    make_pair('f', 2), make_pair('g', 1), make_pair('h', 2), make_pair('i', 1), make_pair('j', 3),
    make_pair('k', 3), make_pair('l', 2), make_pair('m', 1), make_pair('n', 1), make_pair('o', 1),
    make_pair('p', 2), make_pair('q', 2), make_pair('r', 1), make_pair('s', 1), make_pair('t', 1),
    make_pair('u', 1), make_pair('v', 2), make_pair('w', 2), make_pair('x', 3), make_pair('y', 2),
    make_pair('z', 3)
};

// スコアを計算
vector<pair<string, int>> calculate_scores (set<string> anagrams) {
    vector<pair<string, int>> out_put;
    for (string ana: anagrams) {
        int score = 0;
        for (char c: ana) {
            score += letters_score.at(c);
        }
        out_put.push_back(make_pair(ana,score));
    }
    return out_put;
}

// 点数比較、同じ場合は長さ比較
bool comp(pair<string, int> a, pair<string, int> b) {
    if (a.second != b.second) {
        return a.second > b.second;
    }
    return length_comp(a.first, b.first);
}

bool length_comp(string a, string b) {
    return a.size() > b.size();
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