# ATHENS AFTERDARK v2

## Τι δουλεύει
- PWA, responsive interface, φίλτρα, αναζήτηση, αγαπημένα.
- Ανάγνωση `events.json` χωρίς demo events.
- Αυτόματη συλλογή διαθέσιμων καταχωρίσεων από Ticketmaster Discovery API **μόνο αφού ενεργοποιηθεί**.
- GitHub Actions ενημέρωση ανά 6 ώρες και χειροκίνητη εκτέλεση.

## Ενεργοποίηση αυτόματων events
1. Φτιάξε δωρεάν Ticketmaster Developer account και απόκτησε Discovery API key: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
2. Ανέβασε **όλα τα αρχεία** αυτού του φακέλου σε GitHub repository (συμπεριλαμβανομένου του `.github/workflows/update-events.yml`).
3. Στο GitHub repository: Settings → Secrets and variables → Actions → New repository secret. Όνομα: `TICKETMASTER_API_KEY`. Τιμή: το API key σου. **Μην βάλεις το κλειδί σε HTML/JS ή δημόσιο repository.**
4. Actions → Update Athens events → Run workflow. Το workflow γράφει `events.json` και κάνει commit όταν πετύχει.
5. Στο Netlify, σύνδεσε το site με το GitHub repository (Add new project → Import an existing project → GitHub). Publish directory: `.`. Build command: κενό. Αυτό χρειάζεται για να γίνεται νέο deploy σε κάθε commit. Το αρχικό χειροκίνητο Netlify Drop **δεν ενημερώνεται αυτόματα** από GitHub Actions.
6. Άνοιξε το site και έλεγξε το πράσινο status και τις καταχωρίσεις. Μηδέν events μπορεί να σημαίνει μηδέν διαθέσιμα listings στην πηγή, όχι βλάβη.

## Περιορισμοί
- Το Ticketmaster δεν καλύπτει απαραίτητα όλα τα underground parties στην Αθήνα. Δεν υπάρχει αξιόπιστος τρόπος να υποσχεθούμε «όλα» χωρίς επιπλέον επίσημες πηγές και συμφωνίες.
- Δεν υπάρχει live feed πριν την ενεργοποίηση του κλειδιού και του workflow.
- Οι αναζητήσεις είναι κατά keyword, άρα μπορεί να χάσουν καταχωρίσεις ή να έχουν άσχετα αποτελέσματα. Πάντα ελέγχουμε την επίσημη καταχώριση.
- Η ταξινόμηση είδους είναι προσεγγιστική. Οι ώρες είναι από την πηγή, χωρίς επινόηση.
- Αν το API αποτύχει, το workflow αποτυγχάνει χωρίς να σβήσει τα προηγούμενα δεδομένα.
- Το GitHub Actions schedule ενδέχεται να καθυστερήσει και το Netlify free tier έχει όρια.

## Τοπική δοκιμή σε Mac
`python3 -m http.server 8000` μέσα στον φάκελο και μετά άνοιξε `http://localhost:8000`.
