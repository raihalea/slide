{ pkgs, lib, config, inputs, ... }:

{
  packages = [ pkgs.git ];

  languages.javascript = {
    enable = true;
    package = pkgs.nodejs_24;
    npm.enable = true;
    npm.install.enable = true;
  };

  enterShell = ''
    node --version
  '';

  enterTest = ''
    echo "Running tests"
    node --version | grep --color=auto "v24"
  '';
}
