# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/22.04"
  config.vm.hostname = "django-production.local"

  config.vm.provider "orbstack" do |os|
    os.cpu = 2
    os.memory = "2GB"
  end

  config.vm.network "private_network", ip: "192.168.139.36"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 443, host: 8443
  config.vm.network "forwarded_port", guest: 22, host: 2222
  config.vm.network "forwarded_port", guest: 5432, host: 5433

  config.vm.synced_folder ".", "/vagrant", type: "rsync",
    rsync__exclude: [
      ".git/",
      ".venv/",
      "__pycache__/",
      "*.pyc",
      ".pytest_cache/",
      "node_modules/",
      ".vagrant/",
      "uploads/",
      "static/",
      "logs/",
      ".env",
      ".env.*",
    ]

  config.ssh.forward_agent = true
end
