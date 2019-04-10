cd 058;
for f in *.sph; do ../sph2pipe -f  wav "${f%.*}.sph" "${f%.*}.wav"; done

