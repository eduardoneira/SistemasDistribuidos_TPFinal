#/bin/bash

if [[ "$#" == 0 ]]; then
  echo "ERROR: Hay que especificar el sistema operativo en cual instalar. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

echo "Instalando Postgresql"

if [[ "$1" == "fedora" ]]; then
  dnf install postgresql-server postgresql postgresql-contrib
  postgresql-setup --initdb
  systemctl start postgresql
  echo "Ingrese un password para postgres (poner de contraseña: postgres)"
  echo "Ingrese: \password postgres"
  echo "Siga las instrucciones. Para salir ingrese: \q. Luego cuando quede en bash$ ingrese el comando logout"
  cd ~postgres/
  sudo -i -u postgres psql
  echo "Ahora debe cambiar en el archivo ~postgres/data/pg_hba.conf"
  echo "Donde dice METHOD peer, ident, ident poner todo en md5"
  echo "Reiniciar el servcio con $ systemctl restart postgresql"
  echo "Para crear la base de datos $ sudo -i -u postgres psql -c \"CREATE DATABASE srpl\""
  echo "Luego $ sudo -i -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE srpl to postgres\""

elif [[ "$1" == "arch" ]]; then
  pacman -S postgresql
  mkdir /var/lib/postgres/data
  chown -c -R postgres:postgres /var/lib/postgres
  sudo -i -u postgres
  initdb -D '/var/lib/postgres/data'
  logout
  systemctl start postgresql
elif [[ "$1" == "debian" ]] || [[ "$1" == "ubuntu" ]]; then
  apt-get install postgresql postgresql-contrib
  sudo -i -u postgres
fi
