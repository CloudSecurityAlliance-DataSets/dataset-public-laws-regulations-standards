# 電子政府における調達のために参照すべき暗号のリスト（CRYPTREC暗号リスト / CRYPTREC Ciphers List）

CRYPTREC LS-0001-2022R2（令和５年３月30日 デジタル庁・総務省・経済産業省、最終更新：令和８年３月30日）

## 1. 電子政府推奨暗号リスト (e-Government Recommended Ciphers List)

暗号技術検討会（脚注１）及び関連委員会（以下「CRYPTREC」という。）により安全性（セキュリティ）及び実装性能が確認された暗号技術（脚注２）について、市場における利用実績が十分であるか今後の普及が見込まれると判断され、当該技術の利用を推奨するもののリスト。なお、利用する鍵長について、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注３）の規定に合致しない鍵長を用いた場合には、電子政府推奨暗号リストの暗号技術を利用しているとは見なされないことに留意すること。

- （脚注１）デジタル庁統括官、総務省サイバーセキュリティ統括官及び経済産業省商務情報政策局長が有識者の参集を求め、暗号技術の普及による情報セキュリティ対策の推進を図る観点から、専門家による意見等を聴取することにより、デジタル庁、総務省及び経済産業省における施策の検討に資することを目的として開催。
- （脚注２）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。
- （脚注３）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html なお、当該設定基準の見直しの検討を行う予定であり、当面の間、表２（耐量子計算機暗号（PQC）リスト）の公開鍵暗号は、当該設定基準を適用しない。

### 1.1 表１ 現行暗号リスト (Table 1: Current Ciphers List)

| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |
| --- | --- | --- |
| 公開鍵暗号 | 署名 | DSA（注１） |
| 公開鍵暗号 | 署名 | ECDSA |
| 公開鍵暗号 | 署名 | EdDSA |
| 公開鍵暗号 | 署名 | RSA-PSS |
| 公開鍵暗号 | 署名 | RSASSA-PKCS1-v1_5 |
| 公開鍵暗号 | 守秘 | RSA-OAEP |
| 公開鍵暗号 | 鍵共有 | DH |
| 公開鍵暗号 | 鍵共有 | ECDH（注２） |
| 共通鍵暗号 | 64ビットブロック暗号（注３） | 該当なし |
| 共通鍵暗号 | 128ビットブロック暗号 | AES |
| 共通鍵暗号 | 128ビットブロック暗号 | Camellia |
| 共通鍵暗号 | ストリーム暗号 | KCipher-2 |
| ハッシュ関数 | － | SHA-256 |
| ハッシュ関数 | － | SHA-384 |
| ハッシュ関数 | － | SHA-512 |
| ハッシュ関数 | － | SHA-512/256 |
| ハッシュ関数 | － | SHA3-256 |
| ハッシュ関数 | － | SHA3-384 |
| ハッシュ関数 | － | SHA3-512 |
| ハッシュ関数 | － | SHAKE128（注４） |
| ハッシュ関数 | － | SHAKE256（注４） |
| 暗号利用モード | 秘匿モード | CBC |
| 暗号利用モード | 秘匿モード | CFB |
| 暗号利用モード | 秘匿モード | CTR |
| 暗号利用モード | 秘匿モード | OFB |
| 暗号利用モード | 秘匿モード | XTS（注５） |
| 暗号利用モード | 認証付き秘匿モード（注６） | CCM |
| 暗号利用モード | 認証付き秘匿モード（注６） | GCM（注７） |
| メッセージ認証コード | － | CMAC |
| メッセージ認証コード | － | HMAC |
| 認証暗号 | － | ChaCha20-Poly1305 |
| エンティティ認証 | － | ISO/IEC 9798-2 |
| エンティティ認証 | － | ISO/IEC 9798-3 |
| エンティティ認証 | － | ISO/IEC 9798-4 |

- （注１）FIPS PUB 186-5では廃止されているが、本リスト掲載時から安全性・利用実績の状況に大きな変化がないため、掲載を継続する。
- （注２）使用するMACはHMAC又はCMACに限る。
- （注３）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。
- （注４）ハッシュ長は256ビット以上とすること。
- （注５）ブロック暗号には、CRYPTREC暗号リスト掲載128ビットブロック暗号を使う。利用用途はストレージデバイスの暗号化に限り、実装方法はNIST SP800-38Eに従うこと。
- （注６）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。
- （注７）初期化ベクトル長は96ビットを推奨する。

#### 1.1.1 公開鍵暗号

- **DSA（注１）**（署名）
- **ECDSA**（署名）
- **EdDSA**（署名）
- **RSA-PSS**（署名）
- **RSASSA-PKCS1-v1_5**（署名）
- **RSA-OAEP**（守秘）
- **DH**（鍵共有）
- **ECDH（注２）**（鍵共有）

#### 1.1.2 共通鍵暗号

- **該当なし**（64ビットブロック暗号（注３））
- **AES**（128ビットブロック暗号）
- **Camellia**（128ビットブロック暗号）
- **KCipher-2**（ストリーム暗号）

#### 1.1.3 ハッシュ関数

- **SHA-256**
- **SHA-384**
- **SHA-512**
- **SHA-512/256**
- **SHA3-256**
- **SHA3-384**
- **SHA3-512**
- **SHAKE128（注４）**
- **SHAKE256（注４）**

#### 1.1.4 暗号利用モード

- **CBC**（秘匿モード）
- **CFB**（秘匿モード）
- **CTR**（秘匿モード）
- **OFB**（秘匿モード）
- **XTS（注５）**（秘匿モード）
- **CCM**（認証付き秘匿モード（注６））
- **GCM（注７）**（認証付き秘匿モード（注６））

#### 1.1.5 メッセージ認証コード

- **CMAC**
- **HMAC**

#### 1.1.6 認証暗号

- **ChaCha20-Poly1305**

#### 1.1.7 エンティティ認証

- **ISO/IEC 9798-2**
- **ISO/IEC 9798-3**
- **ISO/IEC 9798-4**

### 1.2 表２ 耐量子計算機暗号（PQC）リスト (Table 2: Post-Quantum Cryptography List)

現行暗号の解読に利用可能な水準の量子計算機（CRQC: Cryptographically Relevant Quantum Computer）への耐性を有することが確認された暗号技術のリスト。

| 技術分類（大分類） | 技術分類（小分類） | 暗号技術（名称） | パラメーターセット（注８） |
| --- | --- | --- | --- |
| 公開鍵暗号 | 署名 | － | － |
| 公開鍵暗号 | 鍵共有 | ML-KEM | ML-KEM-768 (Category 3) ML-KEM-1024 (Category 5) |
| 共通鍵暗号 | － | AES | AES-192 (Category 3) AES-256 (Category 5) |
| ハッシュ関数 | － | SHA2 | SHA-384 (Category 4) SHA-512 |
| ハッシュ関数 | － | SHA3 | SHA3-384 (Category 4) SHA3-512 |

- （注８）セキュリティのカテゴリを合わせて記載する。各カテゴリはNISTの“Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process”に従い、カテゴリ名の右に記載の鍵探索又は衝突探索と同程度以上の計算資源が攻撃に必要であることを意味する（Category 1: 128ビット鍵ブロック暗号、Category 2: 256ビットハッシュ関数、Category 3: 192ビット鍵ブロック暗号、Category 4: 384ビットハッシュ関数、Category 5: 256ビット鍵ブロック暗号）。 https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf （令和８年３月25日現在）
- （脚注４）暗号技術の耐量子計算機暗号（PQC）リストへの追加について検討中である。 https://www.cryptrec.go.jp/report/cryptrec-mt-1501-2026.pdf

## 2. 推奨候補暗号リスト (Candidate Recommended Ciphers List)

CRYPTRECにより安全性及び実装性能が確認され、今後、電子政府推奨暗号リストに掲載される可能性のある暗号技術（脚注５）のリスト。なお、本リストに記載されている暗号技術を利用する際は、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注６）の規定に合致する鍵長を用いることが求められることに留意すること。

- （脚注５）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。
- （脚注６）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html

| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |
| --- | --- | --- |
| 公開鍵暗号 | 署名 | 該当なし |
| 公開鍵暗号 | 守秘 | 該当なし |
| 公開鍵暗号 | 鍵共有 | PSEC-KEM（注９） |
| 共通鍵暗号 | 64ビットブロック暗号（注10） | CIPHERUNICORN-E |
| 共通鍵暗号 | 64ビットブロック暗号（注10） | Hierocrypt-L1 |
| 共通鍵暗号 | 64ビットブロック暗号（注10） | MISTY1 |
| 共通鍵暗号 | 128ビットブロック暗号 | CIPHERUNICORN-A |
| 共通鍵暗号 | 128ビットブロック暗号 | CLEFIA |
| 共通鍵暗号 | 128ビットブロック暗号 | Hierocrypt-3 |
| 共通鍵暗号 | ストリーム暗号 | Enocoro-128v2 |
| 共通鍵暗号 | ストリーム暗号 | MUGI |
| 共通鍵暗号 | ストリーム暗号 | MULTI-S01（注11） |
| ハッシュ関数 | － | 該当なし |
| 暗号利用モード | 秘匿モード | 該当なし |
| 暗号利用モード | 認証付き秘匿モード（注12） | 該当なし |
| メッセージ認証コード | － | PC-MAC-AES |
| 認証暗号 | － | 該当なし |
| エンティティ認証 | － | 該当なし |

- （注９）KEM (Key Encapsulating Mechanism) – DEM (Data Encapsulating Mechanism) 構成における利用を前提とする。
- （注10）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。
- （注11）平文サイズは64ビットの倍数に限る。
- （注12）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。

### 2.1 公開鍵暗号

- **該当なし**（署名）
- **該当なし**（守秘）
- **PSEC-KEM（注９）**（鍵共有）

### 2.2 共通鍵暗号

- **CIPHERUNICORN-E**（64ビットブロック暗号（注10））
- **Hierocrypt-L1**（64ビットブロック暗号（注10））
- **MISTY1**（64ビットブロック暗号（注10））
- **CIPHERUNICORN-A**（128ビットブロック暗号）
- **CLEFIA**（128ビットブロック暗号）
- **Hierocrypt-3**（128ビットブロック暗号）
- **Enocoro-128v2**（ストリーム暗号）
- **MUGI**（ストリーム暗号）
- **MULTI-S01（注11）**（ストリーム暗号）

### 2.3 ハッシュ関数

- **該当なし**

### 2.4 暗号利用モード

- **該当なし**（秘匿モード）
- **該当なし**（認証付き秘匿モード（注12））

### 2.5 メッセージ認証コード

- **PC-MAC-AES**

### 2.6 認証暗号

- **該当なし**

### 2.7 エンティティ認証

- **該当なし**

## 3. 運用監視暗号リスト (Monitored Ciphers List)

実際に解読されるリスクが高まるなど、推奨すべき状態ではなくなったとCRYPTRECにより確認された暗号技術（脚注７）のうち、互換性維持（脚注８）のために継続利用を容認するもののリスト。互換性維持以外の目的での利用は推奨しない。なお、本リストに記載されている暗号技術を利用する際は、「暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準」（脚注９）の規定に合致する鍵長を用いることが求められることに留意すること。

- （脚注７）暗号利用モード、メッセージ認証コード、エンティティ認証は、他の技術分類の暗号技術と組み合わせて利用することとされているが、その場合、CRYPTREC暗号リストに掲載されたいずれかの暗号技術と組み合わせること。
- （脚注８）既に稼働中のシステムやアプリケーション等との間での相互運用を継続すること。
- （脚注９）CRYPTREC, 暗号強度要件（アルゴリズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html

| 技術分類（大分類） | 技術分類（小分類） | 暗号技術 |
| --- | --- | --- |
| 公開鍵暗号 | 署名 | 該当なし |
| 公開鍵暗号 | 守秘 | RSAES-PKCS1-v1_5（注13） |
| 公開鍵暗号 | 鍵共有 | 該当なし |
| 共通鍵暗号 | 64ビットブロック暗号（注14） | 3-key Triple DES（注15） |
| 共通鍵暗号 | 128ビットブロック暗号 | 該当なし |
| 共通鍵暗号 | ストリーム暗号 | 該当なし |
| ハッシュ関数 | － | RIPEMD-160 |
| ハッシュ関数 | － | SHA-1 |
| 暗号利用モード | 秘匿モード | 該当なし |
| 暗号利用モード | 認証付き秘匿モード（注16） | 該当なし |
| メッセージ認証コード | － | CBC-MAC（注17） |
| 認証暗号 | － | 該当なし |
| エンティティ認証 | － | 該当なし |

- （注13）TLS 1.0, 1.1, 1.2で利用実績があることから当面の利用を認める。
- （注14）CRYPTREC暗号リストにおいて、64ビットブロック暗号により、同一の鍵を用いて暗号化する場合、2^20ブロックまで、同一の鍵を用いてCMACでメッセージ認証コードを生成する場合、2^21ブロックまでとする。
- （注15）SP 800-67 Revision 2では廃止されているが、本リスト掲載時から安全性・利用実績の状況に大きな変化がないため、掲載を継続する。
- （注16）CRYPTREC暗号リスト掲載のブロック暗号を、認証付き秘匿モードと組み合わせて、「認証暗号」として使うことができる。
- （注17）安全性の観点から、メッセージ長を固定して利用すべきである。

### 3.1 公開鍵暗号

- **該当なし**（署名）
- **RSAES-PKCS1-v1_5（注13）**（守秘）
- **該当なし**（鍵共有）

### 3.2 共通鍵暗号

- **3-key Triple DES（注15）**（64ビットブロック暗号（注14））
- **該当なし**（128ビットブロック暗号）
- **該当なし**（ストリーム暗号）

### 3.3 ハッシュ関数

- **RIPEMD-160**
- **SHA-1**

### 3.4 暗号利用モード

- **該当なし**（秘匿モード）
- **該当なし**（認証付き秘匿モード（注16））

### 3.5 メッセージ認証コード

- **CBC-MAC（注17）**

### 3.6 認証暗号

- **該当なし**

### 3.7 エンティティ認証

- **該当なし**

## 4. 更新履歴情報 (Revision History)

| 更新日付 | 更新箇所 | 更新前の記述 | 更新後の記述 |
| --- | --- | --- | --- |
| 令和６年 ５月16日 | 注 | ［新規追加］ | （注18）FIPS PUB 186-5では廃止されてい るが、本リスト掲載時から安全性・利用 実績の状況に大きな変化がないため、掲 載を継続する。 |
| 令和６年 ５月16日 | 注 | ［新規追加］ | （注19）SP 800-67 Revision 2では廃止さ れているが、本リスト掲載時から安全 性・利用実績の状況に大きな変化がない ため、掲載を継続する。 |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（本文） | 暗号技術検討会及び関連委員会（以下、 「CRYPTREC」という。）により安全性及 び実装性能が確認された暗号技術につい て、市場における利用実績が十分である か今後の普及が見込まれると判断され、 当該技術の利用を推奨するもののリス ト。 | 暗号技術検討会及び関連委員会（以下 「CRYPTREC」という。）により安全性 （セキュリティ）及び実装性能が確認さ れた暗号技術について、市場における利 用実績が十分であるか今後の普及が見込 まれると判断され、当該技術の利用を推 奨するもののリスト。 |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（表） | ［表の件名付与］ | ＜表１ 現行暗号リスト＞ |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（表） | ［表の新設］ | ＜表２ 耐量子計算機暗号（PQC）リスト＞ 現行暗号の解読に利用可能な水準の量 子計算機（CRQC: Cryptographically Relev ant Quantum Computer）への耐性を有する ことが確認された暗号技術のリスト。 |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（耐量子計 算機暗号（PQC） リスト） | ［技術分類の追加］ | 技術分類：公開鍵暗号－署名 名称／パラメーターセット：－ 技術分類：公開鍵暗号－鍵共有 名称：ML-KEM パラメーターセット： ML-KEM-768 (Category 3) ML-KEM-1024 (Category 5) |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（耐量子計 算機暗号（PQC） リスト） | ［技術分類の追加］ | 技術分類：共通鍵暗号 名称：AES パラメーターセット： AES-192 (Category 3) AES-256 (Category 5) |
| 令和８年 ３月30日 | 電子政府推奨暗号 リスト（耐量子計 算機暗号（PQC） リスト） | ［技術分類の追加］ | 技術分類：ハッシュ関数 名称：SHA2 パラメーターセット： SHA-384 (Category 4) SHA-512 名称：SHA3 パラメーターセット： SHA3-384 (Category 4) SHA3-512 |
| 令和８年 ３月30日 | 脚注 | ５ CRYPTREC, 暗号強度要件（アルゴリ ズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html | ３ CRYPTREC, 暗号強度要件（アルゴリ ズム及び鍵長選択）に関する設定基準, https://www.cryptrec.go.jp/list.html なお、当該設定基準の見直しの検討を行 う予定であり、当面の間、表２（耐量子 計算機暗号（PQC）リスト）の公開鍵暗号 は、当該設定基準を適用しない。 |
| 令和８年 ３月30日 | 脚注 | ［新規追加］ | ４ 暗号技術の耐量子計算機暗号（PQC） リストへの追加について検討中である。 https://www.cryptrec.go.jp/report/cry ptrec-mt-1501-2026.pdf |
| 令和８年 ３月30日 | 脚注 | 脚注３、４、７、８ | 脚注５、７、８、９ |
| 令和８年 ３月30日 | 注 | （注１）「政府機関の情報システムにお いて使用されている暗号アルゴリズム SHA-1及びRSA1024に係る移行指針」（平 成20年４月情報セキュリティ政策会議決 定、平成24年10月情報セキュリティ対策推 進会議改定）を踏まえて利用すること。 https://www.nisc.go.jp/pdf/policy/gen eral/angou ikoushishin.pdf （平成25年３月１日現在） | ［削除］ |
| 令和８年 ３月30日 | 注 | （注８）「政府機関の情報システムにお いて使用されている暗号アルゴリズム SHA-1及びRSA1024に係る移行指針」（平 成20年４月情報セキュリティ政策会議決 定、平成24年10月情報セキュリティ対策推 進会議改定）を踏まえて利用すること。 https://www.nisc.go.jp/pdf/policy/gen eral/angou ikoushishin.pdf （平成25年３月１日現在） | ［削除］ |
| 令和８年 ３月30日 | 注 | ［新規追加］ | （注２）使用するMACはHMACまたはCMACに 限る。 |
| 令和８年 ３月30日 | 注 | ［新規追加］ | （注８）セキュリティのカテゴリを合わ せて記載する。各カテゴリはNIST の “Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process”に従い、次のよう に、カテゴリ名の右に記載の鍵探索又は 衝突探索と同程度以上の計算資源が攻撃 に必要であることを意味する。 ・Category 1 128ビット鍵を持つブロッ ク暗号に対する鍵探索 ・Category 2 256ビットのハッシュ関数 に対する衝突探索 ・Category 3 192ビット鍵を持つブロッ ク暗号に対する鍵探索 ・Category 4 384ビットのハッシュ関数 に対する衝突探索 ・Category 5 256ビット鍵を持つブロッ ク暗号に対する鍵探索 https://csrc.nist.gov/CSRC/media/Projec ts/Post-Quantum-Cryptography/documents/ call-for-proposals-final-dec-2016.pdf （令和８年３月25日現在） |
| 令和８年 ３月30日 | 注 | 注18、２、12、17、13、４、５～７、 14、９、15、19、11 | 注１、３、４、５、６、７、９～11、 12、13、14、15、17 |

## 5. CRYPTREC Ciphers List Overview (English Reference)

CRYPTREC Ciphers List
The list of ciphers that should be referred to in the procurement for the e-Government system (CRYPTREC Ciphers List)
The Digital Agency, MIC and the METI are evaluating the cryptographic technology used in e-Government through the CRYPTREC activity, and decided upon
“The list of ciphers that should be referred to in the procurement for the e-Government system (CRYPTREC Ciphers List)”
(last revision: March 30,2026, CRYPTREC LS-0001-2022R2,
first edition: March 30,2023
).
The CRYPTREC Ciphers List consists of “e-Government Recommended Ciphers List”, “Candidate Recommended Ciphers List” and “Monitored Ciphers List”.
In
“Common Standards for Cybersecurity Measures for Government Agencies and Related Agencies”
(published by Cybersecurity Strategic Headquarters, June 27, 2025, in Japanese),
tentative translation version
, the “e-Government Recommended Ciphers List” is referred as below for information system procurement in governmental organizations.
This list is based on the “CRYPTREC e-Government Recommended Ciphers List” formulated in March 2013(
first edition: March 1,2013
,
last revision: March 8,2023, CRYPTREC LS-0001-2012R8
)was revised. And, CRYPTREC Ciphers List published in March 2013 is a revision
“e-Goverment Recommended Ciphers List”(first edition: Feb. 20,2003)
.
Standards for Cryptographic Strength Requirements (Algorithm and Key Length Selection)
It should be noted that many of the cryptographic techniques on the CRYPTREC Cryptographic List allow multiple key lengths for a single algorithm and that the security strength and efficiency will depend on the key length used.
            So, CRYPTREC decided upon
“Standards for Cryptographic Strength Requirements (Algorithm and Key Length Selection)”
, which specified how to select algorithms and key lengths to achieve appropriate security strength in consideration of the operation period of the information system when using cryptographic techniques listed in the CRYPTREC Ciphers List (First release: March 2022,CRYPTREC LS-0003-2022R1).
Note that, if a key length is used that does not conform to the provisions of this document regarding the key length to be used, it is NOT considered to be using a cryptographic technique on the e-Government Recommended Ciphers List.
Common Standards for Cybersecurity Measures for Government Agencies and Related Agencies (Extract)
Information system security officers shall, based on the “e-Government Recommended Ciphers List” whose security and performance is confirmed by CRYPTREC (the Cryptography Research and Evaluation Committees), establish encryption and digital signature algorithm and key length used on information systems, a safe protocol using them, and operating procedures for methods to operate them.
[References]
Common Model of Cybersecurity Measures for Government Agencies and Related Agencies(FY2025), tentative translation version
Common Standards for Cybersecurity Measures for Government Agencies and Related Agencies(FY2025), tentative translation version
BACK TO TOP

## 6. Cryptographic Technique Evaluation in CRYPTREC

Specifications of CRYPTREC Ciphers List
“The list of ciphers that shoud be referred to in the procurement of the e-Government system(CRYPTREC Ciphers List)”
(last revision: March 30,2026, CRYPTREC LS-0001-2022R2) consists of three lists: “e-Government Recommended Ciphers List”, “Candidate Recommended Ciphers List” and “Monitored Ciphers List”.
The specifications of the ciphers in these lists are shown in the following tables. Please note that the ciphers listed in the “CRYPTREC Ciphers List” are limited to those in the following tables.
            For the specifications of the ciphers in the previous “e-Government Recommended Ciphers List”, please refer to
“Specifications of e-Government Recommended Ciphers”
.
Specifications of ciphers in the e-Government Recommended Ciphers List <Current Ciphers List>
Classification
Cipher
Specification
Public key ciphers
Signature
DSA
NIST FIPS PUB 186-4
ECDSA
SEC 1: Elliptic Curve Cryptography (September 20, 2000 Version 1.0)
(*3)
or
ANSI X9.142-2020, Financial Services - Public Key Cryptography for The Financial Services Industry - The Elliptic Curve Digital Signature Algorithm -ECDSA (*2)
EdDSA
Edwards-Curve Digital Signature Algorithm (EdDSA), RFC 8032 (January, 2017)
or
NIST FIPS PUB 186-5
RSA-PSS
PKCS #1: RSA Cryptography Specifications Version 2.2, RFC 8017 (November, 2016)
RSASSA-PKCS1-v1_5
PKCS #1: RSA Cryptography Specifications Version 2.2, RFC 8017 (November, 2016)
Confidentiality
RSA-OAEP
PKCS #1: RSA Cryptography Specifications Version 2.2, RFC 8017 (November, 2016)
Key exchange
DH
ANSI X9.42-2003, Public Key Cryptography for the Financial Services Industry: Agreement of Symmetric Keys Using Discrete Logarithm Cryptography (*2)
or
Specified as FFC DH primitive in
NIST SP 800-56A Revision 2 (May 2013)
ECDH
SEC 1: Elliptic Curve Cryptography (September 20, 2000 Version 1.0)
(*3)
or
Specified as C(2e, 0s, ECC CDH) in
NIST SP 800-56A Revision 3 (April 2018)
(*4)
Symmetric key ciphers
64-bit block ciphers
NA
128-bit block ciphers
AES
NIST FIPS PUB 197
Camellia
Algorithm specifications of 128-bits block cipher Camelia (2nd version: September 26, 2001)
Stream ciphers
KCipher-2
Stream Cipher KCipher-2 (March 31, 2017 Version1.2)
Hash functions
SHA-256
NIST FIPS PUB 180-4
SHA-384
NIST FIPS PUB 180-4
SHA-512
NIST FIPS PUB 180-4
SHA-512/256
NIST FIPS PUB 180-4
SHA3-256
NIST FIPS PUB 202
SHA3-384
NIST FIPS PUB 202
SHA3-512
NIST FIPS PUB 202
SHAKE128
NIST FIPS PUB 202
SHAKE256
NIST FIPS PUB 202
Modes of operation
Encryption modes
CBC
NIST SP 800-38A
CFB
NIST SP 800-38A
CTR
NIST SP 800-38A
OFB
NIST SP 800-38A
XTS
NIST SP 800-38E
Authenticated encryption modes
CCM
NIST SP 800-38C
GCM
NIST SP 800-38D
Message authentication codes
CMAC
NIST SP 800-38B
HMAC
NIST FIPS PUB 198-1
Authenticated encryption
ChaCha20-Poly1305
ChaCha20 and Poly1305 for IETF Protocols, RFC 8439 (June 2018)
Entity authentication
ISO/IEC 9798-2 (*1)
ISO/IEC 9798-2:2008,
ISO/IEC 9798-2:2008/Cor 1:2010,
ISO/IEC 9798-2:2008/Cor 2:2012,
ISO/IEC 9798-2:2008/Cor 3:2013
ISO/IEC 9798-3 (*1)
ISO/IEC 9798-3:1998,
ISO/IEC 9798-3:1998/Amd 1:2010,
ISO/IEC 9798-3:1998/Cor 1:2009,
ISO/IEC 9798-3:1998/Cor 2:2012
ISO/IEC 9798-4(*1)
ISO/IEC 9798-4:1999，
ISO/IEC 9798-4:1999/Cor 1:2009,
ISO/IEC 9798-4:1999/Cor 2:2012
(*1) Specifications can be purchased from
Japanese Standards Association
.
(*2) Specifications can be purchased from
https://www.x9.org/
.
(*3) A newer version has been published. CRYPTREC is considering the change of reference.
(*4) The message authentication code algorithm shall be selected from HMAC and AES-CMAC.
When a specification is linked to outside of this domain, the specification is managed by the linked organization.
If you find a broken link, please inform it to CRYPTREC Secretariat.
BACK TO TOP
Specifications of ciphers in the e-Government Recommended Ciphers List <PQC List>
Classification
Cipher
Specification
Public key ciphers
Signature
—
—
Key exchange
ML-KEM
NIST FIPS PUB 203
Symmetric key ciphers
AES
NIST FIPS PUB 197
Hash functions
SHA-384
NIST FIPS PUB 180-4
SHA-512
NIST FIPS PUB 180-4
SHA3-384
NIST FIPS PUB 202
SHA3-512
NIST FIPS PUB 202
When a specification is linked to outside of this domain, the specification is managed by the linked organization.
              If you find a broken link, please inform it to CRYPTREC Secretariat.
BACK TO TOP
Specifications of ciphers in the Candidate Recommended Ciphers List
Classification
Cipher
Specification
Public key ciphers
Signature
NA
Confidentiality
NA
Key exchange
PSEC-KEM
PSEC-KEM specification (April 14, 2008)
Symmetric key ciphers
64-bit block ciphers
CIPHERUNICORN-E
Cryptographic specifications CIPHERUNICORN-E (May 8, 2002)
Hierocrypt-L1
Cryptographic specifications :Hierocrypt-L1 (May 2002)
MISTY1
Cryptographic specifications MISTY1 (updated May 13, 2002)
128-bit block ciphers
CIPHERUNICORN-A
Cryptographic specifications CIPHERUNICORN-A (May 8, 2002)
CLEFIA
The 128-bit Blockcipher CLEFIA Specification Version 1.0 (January 29, 2010)
Hierocrypt-3
Specification on a Block Cipher : Hierocrypt-3 (May 2002)
Stream ciphers
MUGI
Pseudo random number generator MUGI specifications, version 1.3 (May 14, 2002)
Enocoro-128v2
Pseudorandom Number Generator Enocoro, Specification Ver. 2.0 (2 February 2010)
MULTI-S01
Specifications MULTI-S01; Ciphers, Version 1.2 (May 14, 2002)
Hash functions
NA
Modes of operation
Encryption modes
NA
Authenticated encryption modes
NA
Message authentication codes
PC-MAC-AES
Specification of Cryptographic Technique PC-MAC-AES (February 3, 2010)
Authenticated encryption
NA
Entity authentication
NA
When a specification is linked to outside of this domain, the specification is managed by the linked organization.
If you find a broken link, please inform it to CRYPTREC Secretariat.
BACK TO TOP
Specifications of ciphers in the Monitored Ciphers List
Classification
Cipher
Specification
Public key ciphers
Signature
NA
Confidentiality
RSAES-PKCS1-v1_5
PKCS #1: RSA Cryptography Specifications Version 2.2, RFC 8017 (November, 2016)
Key exchange
NA
Symmetric key ciphers
64-bit block ciphers
3-key Triple DES
NIST SP 800-67 Revision 2 (November 2017)
128-bit block ciphers
NA
Stream ciphers
NA
Hash functions
RIPEMD-160
The hash function RIPEMD-160
SHA-1
NIST FIPS PUB 180-4
Modes of operation
Encryption modes
NA
Authenticated encryption modes
NA
Message authentication codes
CBC-MAC
ISO/IEC 9797-1:2011 (*1)
Authenticated encryption
NA
Entity authentication
NA
(*1) Specifications can be purchased from
Japanese Standards Association
.
When a specification is linked to outside of this domain, the specification is managed by the linked organization.
              If you find a broken link, please inform it to CRYPTREC Secretariat.
Contact: CRYPTREC Secretariat
BACK TO TOP
