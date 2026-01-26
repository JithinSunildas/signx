{
  description = "A collaborative Python development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          (pkgs.python3.withPackages (
            ps: with ps; [
              numpy
              pandas
              matplotlib
              scikit-learn
            ]
          ))
        ];

        shellHook = ''
          export PYTHONPATH="$PYTHONPATH:$(pwd)"
          echo "Welcome to your reproducible Python environment!"
          python --version
        '';
      };
    };
}
