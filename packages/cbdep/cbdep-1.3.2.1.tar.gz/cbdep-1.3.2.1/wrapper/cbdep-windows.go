package main

import (
	"io"
	"fmt"
	"net/http"
	"os"
	"os/exec"
)

func main() {
	url := "https://s3.amazonaws.com/packages.couchbase.com/cbdep/install-cbdep.ps1"

	// Set the path to cbdep and check if it exists
	cbdep := fmt.Sprintf("%s\\.local\\bin\\cbdep.exe", os.Getenv("USERPROFILE"))

	if _, err := os.Stat(cbdep); os.IsNotExist(err) {
		// Download the Powershell script and pipe it to PowerShell
		resp, err := http.Get(url)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()
		cmd := exec.Command("powershell", "-ExecutionPolicy", "Bypass", "-Command", "-")
		cmd.Stdin = resp.Body
		cmd.Stdout = io.Discard
		cmd.Stderr = io.Discard

		err = cmd.Run()
		if err != nil {
			panic(err)
		}
	}

	// Run cbdep, passing all of our arguments
	cmd := exec.Command(cbdep, os.Args[1:]...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}
