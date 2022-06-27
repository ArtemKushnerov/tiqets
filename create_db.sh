mysql -h $DB_HOST -u root -e "DROP DATABASE IF EXISTS tiqets"
mysql -h $DB_HOST -u root -e "DROP DATABASE IF EXISTS test_tiqets"
mysql -h $DB_HOST -u root -e "CREATE DATABASE tiqets"
mysql -h $DB_HOST -u root -e "CREATE DATABASE test_tiqets"
