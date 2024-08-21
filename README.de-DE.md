# apetito-menu-downloader
Einfaches Python-Programm, das Menüpläne von Apetito herunterladen kann

## Verwendung
Dieses Programm lädt ein Menü vom Essenslieferanten Apetito herunter und fügt die Daten in eine vordefinierte Vorlage ein. Es ist für HTML optimiert, sodass Sie die Daten z. B. auf einem Bildschirm anzeigen können, damit alle Mitarbeiter/Schüler sie sehen können. Es kann auch verwendet werden, um einen Aushang zusammenzustellen.

## Einrichtung
**Bitte beachten:** Wenn Sie diese Anweisungen verstehen, können Sie jeden Browser verwenden, der sie unterstützt. <br> Sie wurden für Firefox geschrieben, wenn Sie sie also nicht verstehen, *verwenden Sie bitte Firefox!*
1. Laden Sie die Datei starterpack.zip des neuesten Release herunter und entpacken Sie sie.
1. Gehen Sie in einem Browser zu dem Plan, den Sie anzeigen möchten, und klicken Sie auf „Ausdrucken“.
2. Wählen Sie dort „Aushang drucken“ und nehmen Sie die entsprechenden Einstellungen vor.
3. Danach sollten Sie eine Schaltfläche mit der Bezeichnung „Excel exportieren“ finden. *Bevor* Sie darauf klicken, drücken Sie die rechte Maustaste und aktivieren den Inspektionsmodus (Q). Dort öffnen Sie den Tab "Netzwerkanalyse". Wenn Sie es gefunden haben, drücken Sie den Excel-Export.
4. Die Datei, die Sie jetzt erhalten, ist irrelevant, Sie müssen sie nicht speichern. Wichtig ist, dass jetzt das Paket für den Download in der Dev-Konsole angezeigt werden sollte, oberster Eintrag. Klicken Sie darauf.
5. Rechts sollte sich ein kleines Fenster öffnen, das Informationen zum Paket anzeigt. Kopieren Sie die URL komplett und füge sie in die Konfigurationsdatei (config.py) beim URL-Eintrag (wahrscheinlich ganz oben) ein. ***Die Anführungszeichen müssen bleiben!***
6. Suchen Sie nun (in der Konfiguration) in der URL nach den Einträgen startdate und entdate. Diese sollten ungefähr so ​​aussehen:
   ```
   ...&startdate=123456&enddate=987654&...
   ```
8. Ersetzen Sie die beiden 6-stelligen Zahlen durch zwei geschweifte Klammern ( ```{}``` ). Dadurch kann das Programm den Zeitrahmen des Plans dynamisch ändern. Es sollte ungefähr so ​​aussehen:
   ```
   ...&startdate={}&enddate={}&...
   ```
10. Suchen Sie abschließend im Paketfenster in den Request-Headern (den unteren) nach den Werten Authentication und Cookie.
11. Fügen Sie diese Zeichenfolgen in die Authentifizierungsdatei (auths.txt) ein. Die erste Zeile ist die Authentication, die zweite Zeile das Cookie.

***Achtung!*** Diese Zeichenfolgen können verwendet werden, um *alles* auf Ihrem Konto zu tun, einschließlich Transaktionen und Bestellungen. Sie sollten sie *niemals* an jemanden weitergeben, auch nicht auf Anfrage. Wenn sie dennoch an die Öffentlichkeit geraten sind, gehen Sie sofort zu Ihren Apetito-Kontoeinstellungen und melden Sie sich auf allen Geräten ab. Dies erfordert eine vollständige Wiederholung der Schritte 2-5 und 9-10.

### Die Konfiguration
Die mit dem Starterpaket gelieferte Konfiguration funktioniert in den meisten Fällen. Eine Sache, die Sie vielleicht interessieren könnte, ist die Änderung der Programmsprache, um Monate und Wochentage korrekt anzuzeigen. Ändern Sie einfach den language-Tag in Ihren [POSIX-Sprachcode](https://learn.microsoft.com/en-us/globalization/locale/other-locale-names#posix). Für Deutsch lautet dieser ```'de_DE'```. Die Konfiguration selbst ist zudem kommentiert, sodass Sie dort meistens sehen, was jede Option bewirkt.

Wenn Sie dem Programm eigenen Code hinzufügen möchten, ist es möglicherweise gut zu wissen, dass die gesamte config.py-Datei beim Start ausgeführt wird. Dies bedeutet, dass Sie, wenn Sie eine Funktion, Variablen usw. hinzufügen möchten, diese dort hinzufügen sollten, damit Sie das Programm besser aktualisieren können, wenn eine neue Version herauskommt, da die Konfiguration bei Aktualisierungen bestehen bleibt.

### Das Template
Das Programm verwendet (standardmäßig) die Datei „Template.html“, um seine Daten in eine verwendbare Datei zu kompilieren. Dies funktioniert, indem bestimmte Tags in der Datei durch Daten ersetzt werden:

- ```{a[day]}``` und ```{b[day]}``` Platzhalter für die Menüzeilen, wobei day "Tage ab dem Startdatum bedeutet" (z.B. 0 für das Startdatum)

- ```{d[day]}``` gibt den Tag an.

- ```{m[day]}``` gibt den Monat oder den Inhalt von monthEmpty (siehe oben) an.

- ```{wd[day]}``` gibt den Wochentag an.

- ```{ts}``` gibt den Zeitstempel des Plans an. Das Format kann mit tsTimeFormat angegeben werden.

- ```{kw}``` gibt die Kalenderwoche an.

Das Starterpaket enthält auch eine Beispielvorlage, damit Sie ein Gefühl für die Syntax bekommen.

Wenn weitere Platzhalter benötigt werden, können Sie diese gerne in Zeile 91 einfügen.

## Probleme?

Sollten Probleme oder Fehler auftreten, können Sie gerne [ein Problem melden](https://github.com/Josua-P/apetito-menu-downloader/issues). Ich werde versuchen, Ihnen so schnell wie möglich zu helfen!
