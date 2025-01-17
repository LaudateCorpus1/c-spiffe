# Release

This directory contain the files to run a cosign release.

# Signing and Uploading Other Types

This documentation contains information on how to sign and upload data in different pluggable types.

## Minisign

Create a keypair with something like:

```console
$ minisign -G
Please enter a password to protect the secret key.

Password:
Password (one more time):
Deriving a key from the password in order to encrypt the secret key... done

The secret key was saved as $HOME/.minisign/minisign.key - Keep it secret!
The public key was saved as minisign.pub - That one can be public.

```

Sign a file:

```console
$ minisign -S -m c-spiffe-1.0.0.tar.gz
Password:
Deriving a key from the password and decrypting the secret key... done
```

Upload to rekor:

```console
$ rekor-cli upload --artifact c-spiffe-1.0.0.tar.gz --signature c-spiffe-1.0.0.tar.gz.minisig --pki-format=minisign --public-key=minisign.pub
Created entry at index 272756, available at: https://rekor.sigstore.dev/api/v1/log/entries/da528f78c3b1c8e05f0a4b643ad189015d5784ebc8c1c060e807fcfae471e07d
```

Look at the entry with:

```console
$ rekor-cli get --uuid=da528f78c3b1c8e05f0a4b643ad189015d5784ebc8c1c060e807fcfae471e07d
LogID: c0d23d6ad406973f9559f3ba2d1ca01f84147d8ffc5b8445c224f98b9591801d
Index: 272756
IntegratedTime: 2021-08-18T12:42:27Z
UUID: da528f78c3b1c8e05f0a4b643ad189015d5784ebc8c1c060e807fcfae471e07d
Body: {
  "RekordObj": {
    "data": {
      "hash": {
        "algorithm": "sha256",
        "value": "d21f151e5a940cc135084b3092d8ed89be88208848b5916f480ebcefd725f9ba"
      }
    },
    "signature": {
      "content": "dW50cnVzdGVkIGNvbW1lbnQ6ClJXUWoyRUtnVU5vWlYybTlva0tpSzZhaUF1d29KdzhtQjZvaTlIakRXQ3hTcGNQMGxZL3JxUERpM01oSVpJUUVVTWZaTml5TFh2eDQ5Q1RjSC9vTHRoOEZXejZiV2x2dytBMD0=",
      "format": "minisign",
      "publicKey": {
        "content": "NTh3QW1MTjZOYnZnT2dXODMwelM1MUxVa0FNQ3Jsbjc4ems0Y1Bzd3Aydz0="
      }
    }
  }
}

```

Verify a file
```shell
rekor-cli verify --artifact c-spiffe-1.0.0.tar.gz --pki-format=minisign --public-key minisign.pub 
a detached signature must be provided
```


>### Issue opened
>Using rekor-cli verify given just the --artifact and --public-key #416
>https://github.com/sigstore/rekor/issues/416


## Generate a keypair

```shell
$ cosign generate-key-pair
Enter password for private key:
Enter again:
Private key written to cosign.key
Public key written to cosign.pub
```

## sign-blob and verify-blob

```shell
$ cosign sign-blob -key cosign.key c-spiffe-1.0.0.tar.gz > c-spiffe-1.0.0.tar.gz.sig
Using payload from: c-spiffe-1.0.0.tar.gz
Enter password for private key:
```

We can check the pass of the key
```shell
$ cosign verify-blob -key cosign.pub -signature MEYCIQDvdgjw9pIVCZgFIRFQCyOqhTBfbiBNbaE0+a7Mp8U1eAIhAP66aQ54PgzZ3xYvqlrwKMAk998OcnCXsNuDxc2Gjctb c-spiffe-1.0.0.tar.gz
Verified OK
```

as well as the pass of the signuture file
```shell
$ cosign verify-blob -key cosign.pub -signature c-spiffe-1.0.0.tar.gz.sig c-spiffe-1.0.0.tar.gz
Verified OK
```



