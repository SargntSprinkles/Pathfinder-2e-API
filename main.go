package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/SargntSprinkles/Pathfinder-2e-API/pathfinder/ancestries"
	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", rootHandler)
	router.HandleFunc("/ancestries/", ancestries.List)
	router.HandleFunc("/ancestries/{name}", ancestries.Get)
	log.Fatal(http.ListenAndServe(":8080", router))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Pathfinder 2e API!\nAll data comes directly from Archives of Nethys\n%s", r.URL.Path[1:])
}
