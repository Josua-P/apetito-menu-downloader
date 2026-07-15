# apetito-menu-downloader
Einfaches Python-Programm, das Menüpläne von Apetito herunterladen kann

[English readme](https://github.com/Josua-P/apetito-menu-downloader/blob/main/README.md)

## Verwendung
Dieses Programm lädt ein Menü vom Essenslieferanten Apetito herunter und fügt die Daten in eine vordefinierte Vorlage ein. Es ist für HTML optimiert, sodass Sie die Daten z. B. auf einem Bildschirm anzeigen können, damit alle Mitarbeiter/Schüler sie sehen können. Es kann auch verwendet werden, um einen Aushang zusammenzustellen.

## Einrichtung
**Bitte beachten:** Wenn Sie diese Anweisungen verstehen, können Sie jeden Browser verwenden, der sie unterstützt. <br> Sie wurden für Firefox geschrieben, wenn Sie sie also nicht verstehen, *verwenden Sie bitte Firefox!*
1. Laden Sie die Datei starterpack.zip des neuesten Release herunter und entpacken Sie sie.
1. Gehen Sie in einem Browser zu dem Plan, den Sie anzeigen möchten, und klicken Sie auf „Drucken“.
2. Wählen Sie dort den Dokumenttyp „Speiseplan“ und den Dateityp "CSV". Merken Sie sich das eingestellte Startdatum.
3. Danach sollten Sie eine Schaltfläche mit der Bezeichnung „Erstellen“ finden. *Bevor* Sie darauf klicken, drücken Sie die rechte Maustaste und aktivieren den Inspektionsmodus (Q). Dort öffnen Sie den Tab "Netzwerkanalyse". Wenn Sie es gefunden haben, drücken Sie den Export.
4. Die Datei, die Sie jetzt erhalten, ist irrelevant, Sie müssen sie nicht speichern. Wichtig ist, dass jetzt das Paket für den Download in der Dev-Konsole angezeigt werden sollte. Sie sollten 2 Pakete sehen, eines davon hat den Typ "GET". Klicken Sie auf dieses.
5. Rechts sollte sich ein kleines Fenster öffnen, das Informationen zum Paket anzeigt. Kopieren Sie die ID, die sich nach "mealmaster.apetito.com/api/printing-configurations" befindet, bis zum nächsten Schrägstrich und fügen Sie sie in die Konfigurationsdatei (config.py) beim ID-Eintrag (wahrscheinlich ganz oben) ein. ***Die Anführungszeichen müssen bleiben!***<br>
Der Eintrag sollte nun wie folgt aussehen:<br><br>
   ```
   ID = "12345678-abcd-cdef-1357-2468acef4321"
   ```
6. Suchen Sie nun in der URL nach dem Eintrag startOffset. Dieser sollte eine Nummer haben.
7. Jetzt müssen Sie ein wenig rechnen: Ziehen Sie von ihrem eingestellten Startdatum die angegebene Zahl an Tagen ab. <br>Z.B.: Bei einem eingestellten Startdatum 26.7.2026 und einem Offset von 15 wäre ihr Ergebnis der 11.7.2026.
8. Dieses Datum müssen Sie nun in der Config eintragen:<br><br>
   ```
   initDate = datetime.date(<Jahr>, <Monat>, <Tag>)
   ```
   Z.B. wäre der 11.7.2026 notiert mit:<br><br>
   ```
   datetime.date(2026, 7, 11)
   ```
10. Suchen Sie abschließend im Paketfenster in den Request-Headern (den unteren) nach dem Wert Authentication.
11. Fügen Sie diese Zeichenfolge in die Authentifizierungsdatei (auths.txt) ein.

***Achtung!*** Diese Zeichenfolge kann verwendet werden, um *alles* auf Ihrem Konto zu tun, einschließlich Transaktionen und Bestellungen. Sie sollten sie *niemals* an jemanden weitergeben, auch nicht auf Anfrage. Wenn sie dennoch an die Öffentlichkeit geraten ist, ändern Sie *sofort* ihr Passwort. Dies erfordert eine vollständige Wiederholung der Schritte 2-10.

### Die Konfiguration
Die mit dem Starterpaket gelieferte Konfiguration funktioniert in den meisten Fällen. Eine Einstellung, die Sie vielleicht interessieren könnte, ist die Änderung der Programmsprache, um Monate und Wochentage korrekt anzuzeigen. Ändern Sie einfach den language-Tag in Ihren [POSIX-Sprachcode](https://learn.microsoft.com/en-us/globalization/locale/other-locale-names#posix). Für Deutsch lautet dieser ```'de_DE.utf8'```. Die Konfiguration selbst ist zudem kommentiert, sodass Sie dort meistens sehen, was jede Option bewirkt.

Wenn Sie dem Programm eigenen Code hinzufügen möchten, ist es möglicherweise gut zu wissen, dass die gesamte config.py-Datei beim Start ausgeführt wird. Dies bedeutet, dass Sie, wenn Sie eine Funktion, Variablen usw. hinzufügen möchten, diese dort hinzufügen sollten, damit Sie das Programm besser aktualisieren können, wenn eine neue Version herauskommt, da die Konfiguration bei Aktualisierungen bestehen bleibt.

### Das Template
Das Programm verwendet (standardmäßig) die Datei „Template.html“, um seine Daten in eine verwendbare Datei zu kompilieren. Dies funktioniert, indem bestimmte Tags in der Datei durch Daten ersetzt werden:

- ```{a[day]}``` und ```{b[day]}``` Platzhalter für die Menüzeilen, wobei day "Tage ab dem Startdatum bedeutet" (z.B. 0 für das Startdatum)

- ```{d[day]}``` gibt den Tag an.

- ```{m[day]}``` gibt den Monat oder den Inhalt von monthEmpty (siehe config) an.

- ```{wd[day]}``` gibt den Wochentag an.

- ```{ts}``` gibt den Zeitstempel des Plans an. Das Format kann mit tsTimeFormat angegeben werden.

- ```{kw}``` gibt die Kalenderwoche an.

Das Starterpaket enthält auch eine Beispielvorlage, damit Sie ein Gefühl für die Syntax bekommen.

Wenn weitere Platzhalter benötigt werden, können Sie diese gerne in Zeile 171 einfügen.

## Probleme?

Sollten Probleme oder Fehler auftreten, können Sie gerne [ein Problem melden](https://github.com/Josua-P/apetito-menu-downloader/issues). Ich werde versuchen, Ihnen so schnell wie möglich zu helfen!

## KI-Hinweis

Dieses Programm wurde ohne den Einsatz von künstlicher Intelligenz erstellt.
