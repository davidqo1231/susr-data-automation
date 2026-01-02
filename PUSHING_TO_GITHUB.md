# Ako dostať lokálne commity na GitHub

Tieto kroky predpokladajú, že máte otvorenú stránku vášho repozitára na GitHube a používate príkazový riadok v tomto kontajneri (kde už sú commity vytvorené).

## 1) Skopírujte URL vášho repozitára
1. Na stránke repozitára kliknite na zelené tlačidlo **Code**.
2. Skopírujte adresu z tabu **HTTPS** (vyzerá napr. `https://github.com/<vas-ucet>/<repo>.git`).

## 2) Pridajte remote (ak ešte nie je)
V termináli v koreňovom priečinku projektu spustite:

```bash
git remote -v
```

- Ak nič nevráti, pridajte remote:

```bash
git remote add origin https://github.com/<vas-ucet>/<repo>.git
```

## 3) Nastavte meno vetvy a pushnite
Aktuálna vetva je `work`. Na GitHub ju dostanete príkazom:

```bash
git push -u origin work
```

- Pri prvom pushi vás Git vyzve na prihlasovacie údaje. Pri HTTPS zadajte:
  - **Username:** vaše GitHub meno
  - **Password:** Personal Access Token (PAT) s právom `repo`. Ak ho ešte nemáte, na GitHube kliknite na svoj avatar > **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)** > **Generate new token** a zaškrtnite `repo`. Token si skopírujte a použite ako heslo.

## 4) Overte, že je commit na GitHube
Po úspešnom pushi obnovte stránku repozitára. V zozname vetiev by sa mala objaviť `work` a v nej commit s názvom **Improve downloader robustness**.

## 5) Voliteľné: vytvorte pull request
Ak chcete zmeniť predvolenú vetvu (napr. `main`), na stránke GitHubu kliknite na **Compare & pull request** pri vetve `work` a vytvorte PR.
