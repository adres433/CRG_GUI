# CRG - Cccam Reader GUI

### Table of content

- [Description EN](#description-pl)
- [Technologies](#technologies)
- [How start](#how-start)
- [Description PL](#description-pl)

### DESCRIPTION EN

	This app is a graphical equivalent [cccamReader](https://github.com/adres433/cccam_reader)

	In application can change configuration  of readers always before generate readers,
	so is more universal and can many different update readers with diffrent configuration.

	Additionally in app is implemented connection with FTP server in SAT decoder with Enigma2, 
	which allow readers update directly from app.
	Enaught give host adress, port and password to FTP.
	
	SCREEN:
	![Main screen](/screen/main.png)
	![Config screen](/screen/cfg.png)

### TECHNOLOGIES

	- PYTHON: tkinter, ftplib

### HOW START

	- Run .exe file from [output](/output)
	- Click "USTAWIENIA" and write your reader set:
	'''
		option1 = value1
		option2 = value2
		option3 = value3
		...
	'''
	- Set FTP addres and port (111.222.333.444:1234)
		or lieave empty fields - then app will open file with generated 
		readers and don't update them at SAT decoder
	- Click "GENERUJ"
	- Paste Cline according to template: '''C: HOST PORT USER PWD'''
	- Click "GENERUJ" and automaticaly update your readers in SAT decoder
			or open file with your readers to paste in your oscam.

### DESCRIPTION PL

	Aplikacja jest graficznym odpowiednikiem [cccamReader](https://github.com/adres433/cccam_reader)

	W aplikacji możemy zmienić konfigurację czytników przed każdym generowaniem,
	co pozwala generowac czytniki dla różnych dekoderów o różnych konfiguracjach czytników
	i czyni to aplikację bardziej uniwersalną.
	
	Dodatkowo w aplikacji zaimplementowana jest komunikacja z serwerem FTP
	dekodera satelitarnego z Enigma2.
	Pozwala to na automatyczną aktualizację czytników na wybranym dekoderze.
	Wystarczy wprowadzić dane serwera FTP takie jak adres, port i hasło.