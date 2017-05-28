sudo apt-get install python-pip
sudo pip install beautifulsoup4
http://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosHistorico
http://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosActivos

curl 'https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosyCargosActivosPorId_Legislador' -H 'Accept: application/xml, text/xml, */*; q=0.01' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Host: parlamentaria.legislatura.gov.ar' -H 'Origin: http://www.legislatura.gov.ar' -H 'Referer: http://www.legislatura.gov.ar/legislador.php?id=30774' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --data 'id_legislador=30774'

curl 'https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosActivosNuevo' -H 'Accept: application/xml, text/xml, */*; q=0.01' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Host: parlamentaria.legislatura.gov.ar' -H 'Origin: http://www.legislatura.gov.ar' -H 'Referer: http://www.legislatura.gov.ar/legisladores.php' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' --data 'id_bloque='

https://docs.python.org/2/library/xml.etree.elementtree.html