#!/bin/bash

function terraform-install() {
  sudo -i -u vagrant

  cd /vagrant/stack/local/"$1"
  echo -e '\e[38;5;198m'"++++ terraform init.."
  terraform init
  echo -e '\e[38;5;198m'"++++ terraform fmt.."
  terraform fmt
  echo -e '\e[38;5;198m'"++++ terraform validate.."
  terraform validate
  echo -e '\e[38;5;198m'"++++ terraform plan.."
  terraform plan
  echo -e '\e[38;5;198m'"++++ terraform apply.."
  terraform apply --auto-approve
  echo -e '\e[38;5;198m'"++++ awslocal s3 ls.."

  cd /vagrant/stack/
  export PATH=$HOME/.local/bin:$PATH
  awslocal s3 ls
}

terraform-install $1
