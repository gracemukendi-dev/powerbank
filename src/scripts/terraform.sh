#!/bin/bash

function terraform-install() {
  sudo -i -u vagrant
  if [ -f /usr/local/bin/terraform ]; then
    echo -e '\e[38;5;198m'"++++ `/usr/local/bin/terraform version` already installed at /usr/local/bin/terraform"
  else
    LATEST_URL=$(curl -sL https://releases.hashicorp.com/terraform/index.json | jq -r '.versions[].builds[].url' | sort -t. -k 1,1n -k 2,2n -k 3,3n -k 4,4n | egrep -v 'rc|beta' | egrep 'linux.*amd64' | sort -V | tail -n1)
    wget -q $LATEST_URL -O /tmp/terraform.zip
    mkdir -p /usr/local/bin
    (cd /usr/local/bin && unzip /tmp/terraform.zip)
    echo -e '\e[38;5;198m'"++++ Installed: `/usr/local/bin/terraform version`"
  fi
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
