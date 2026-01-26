{
  description = "Python FHS Environment for Mediapipe";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in
    {
      devShells.${system}.default =
        (pkgs.buildFHSEnv {
          name = "mediapipe-env";

          targetPkgs =
            pkgs:
            (with pkgs; [
              # Python
              python311
              python311Packages.pip
              python311Packages.virtualenv

              # Core System Libraries
              libGL
              libglvnd
              glib
              opencv
              stdenv.cc.cc.lib
              zlib
              glibc

              # X11 & GUI Libraries (Added libxcb here)
              xorg.libxcb
              xorg.libX11
              xorg.libXext
              xorg.libXi
              xorg.libXrender
              xorg.libICE
              xorg.libSM

              # Wayland/common libs (Good to have since you use niri)
              libxkbcommon
              dbus
              wayland

              # Audio
              espeak-ng
            ]);

          runScript = "bash";

          profile = ''
            export CUDA_PATH=""
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:/usr/lib64:$LD_LIBRARY_PATH"
            # Force OpenCV to use X11 backend (runs via XWayland on niri)
            export QT_QPA_PLATFORM=xcb 

            echo "================================================"
            echo "   Mediapipe FHS Environment (v2 - Fixed XCB)"
            echo "================================================"
          '';
        }).env;
    };
}
