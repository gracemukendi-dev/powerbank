# -*- mode: ruby -*-
# vi: set ft=ruby :

# create local domain name e.g user.local.dev
user = ENV["USER"].downcase
fqdn = ENV["fqdn"] || "service.consul"

# https://www.virtualbox.org/manual/ch08.html
vbox_config = [
  { '--memory' => '4096' },
  { '--cpus' => '2' },
  { '--cpuexecutioncap' => '100' },
  { '--biosapic' => 'x2apic' },
  { '--ioapic' => 'on' },
  { '--largepages' => 'on' },
  { '--natdnshostresolver1' => 'on' },
  { '--natdnsproxy1' => 'on' },
  { '--nictype1' => 'virtio' },
  { '--audio' => 'none' },
]

# machine(s) hash
machines = [
  {
    :name => "powerbank.#{fqdn}",
    :ip => '10.9.99.10',
    :ssh_port => '2255',
    :disksize => '10GB',
    :vbox_config => vbox_config,
    :synced_folders => [
      { :vm_path => '/data', :ext_rel_path => '../../', :vm_owner => 'ubuntu' },
    ],
  }
]


Vagrant::configure("2") do |config|

  # check for vagrant version
  Vagrant.require_version ">= 1.9.7"

  if Vagrant::Util::Platform.windows?
    COMMAND_SEPARATOR = "&"
  else
    COMMAND_SEPARATOR = ";"
  end

  # auto install plugins, will prompt for admin password on 1st vagrant up
  required_plugins = %w( vagrant-disksize )
  required_plugins.each do |plugin|
    exec "vagrant plugin install #{plugin}#{COMMAND_SEPARATOR}vagrant #{ARGV.join(" ")}" unless Vagrant.has_plugin? plugin || ARGV[0] == 'plugin'
  end

  machines.each_with_index do |machine, index|

    config.vm.box = "ubuntu/bionic64"
    config.vm.define machine[:name] do |config|

      config.disksize.size = machine[:disksize]
      config.ssh.forward_agent = true
      config.ssh.insert_key = true
      config.vm.network "private_network", ip: machine[:ip]
      config.vm.network "forwarded_port", guest: 22, host: machine[:ssh_port], id: 'ssh', auto_correct: true

      if machines.size == 1 # only expose these ports if 1 machine, else conflicts
        config.vm.network "forwarded_port", guest: 8200, host: 8200 # vault
        config.vm.network "forwarded_port", guest: 3333, host: 3333 # docsify
        config.vm.network "forwarded_port", guest: 4566, host: 4566 # localstack
      end

      config.vm.hostname = "#{machine[:name]}"

      unless machine[:vbox_config].nil?
        config.vm.provider :virtualbox do |vb|
          machine[:vbox_config].each do |hash|
            hash.each do |key, value|
              vb.customize ['modifyvm', :id, "#{key}", "#{value}"]
            end
          end
        end
      end

      # mount the shared folder inside the VM
      unless machine[:synced_folders].nil?
        machine[:synced_folders].each do |folder|
          config.vm.synced_folder "#{folder[:ext_rel_path]}", "#{folder[:vm_path]}", owner: "#{folder[:vm_owner]}", mount_options: ["dmode=777,fmode=777"]
          # below will mount shared folder via NFS
          # config.vm.synced_folder "#{folder[:ext_rel_path]}", "#{folder[:vm_path]}", nfs: true, nfs_udp: false, mount_options: ['nolock', 'noatime', 'lookupcache=none', 'async'], linux__nfs_options: ['rw','no_subtree_check','all_squash','async']
        end
      end

      # vagrant up --provision-with bootstrap to only run this on vagrant up
      config.vm.provision "bootstrap", preserve_order: true, type: "shell", privileged: true, inline: <<-SHELL
        echo -e '\e[38;5;198m'"BEGIN BOOTSTRAP $(date '+%Y-%m-%d %H:%M:%S')"
        echo -e '\e[38;5;198m'"running vagrant as #{user}"
        echo -e '\e[38;5;198m'"vagrant IP "#{machine[:ip]}
        echo -e '\e[38;5;198m'"vagrant fqdn #{machine[:name]}"
        echo -e '\e[38;5;198m'"vagrant index #{index}"
        cd ~\n
        grep -q "VAGRANT_IP=#{machine[:ip]}" /etc/environment
        if [ $? -eq 1 ]; then
          echo "VAGRANT_IP=#{machine[:ip]}" >> /etc/environment
        else
          sed -i "s/VAGRANT_INDEX=.*/VAGRANT_INDEX=#{index}/g" /etc/environment
        fi
        grep -q "VAGRANT_INDEX=#{index}" /etc/environment
        if [ $? -eq 1 ]; then
          echo "VAGRANT_INDEX=#{index}" >> /etc/environment
        else
          sed -i "s/VAGRANT_INDEX=.*/VAGRANT_INDEX=#{index}/g" /etc/environment
        fi
        # install applications
        export DEBIAN_FRONTEND=noninteractive
        export PATH=$PATH:/root/.local/bin
        sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes update -o Acquire::CompressionTypes::Order::=gz
        sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes upgrade
        sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes install swapspace jq curl unzip software-properties-common bzip2 git make python3-pip python3-dev python3-virtualenv golang-go apt-utils
        sudo -E -H pip3 install pip --upgrade
        sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes autoremove
        sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes clean
        sudo rm -rf /var/lib/apt/lists/partial
         
        #powerbank global config
        echo "Configuring Powerbank Globals and Logging. Check the /vagrant/powerbank.log to ensure all went well."
        python3 /vagrant/src/globals.py

        echo -e '\e[38;5;198m'"END BOOTSTRAP $(date '+%Y-%m-%d %H:%M:%S')"
      SHELL

      # install docker
      # vagrant up --provision-with docker to only run this on vagrant up
      config.vm.provision "docker", preserve_order: true, type: "shell", path: "docker/docker.sh"

      # install vault
      # vagrant up --provision-with vault to only run this on vagrant up
      config.vm.provision "vault", type: "shell", preserve_order: true, privileged: true, path: "hashicorp/vault.sh"

      # install packer
      # vagrant up --provision-with packer to only run this on vagrant up
      config.vm.provision "packer", type: "shell", preserve_order: true, privileged: true, path: "hashicorp/packer.sh"

      # install powerbank localstack
      # vagrant up --provision-with localstack to only run this on vagrant up
      config.vm.provision "powerlocal", type: "shell", preserve_order: true, privileged: false, inline: "python3 /vagrant/src/main.py"

      # docsify
      # vagrant up --provision-with docsify to only run this on vagrant up
      config.vm.provision "docsify", type: "shell", preserve_order: true, privileged: false, path: "docsify/docsify.sh"
    end
  end
end
