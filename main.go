package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/SargntSprinkles/Pathfinder-2e-API/pathfinder/ancestries"
	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", rootHandler)
	router.HandleFunc("/ancestries/", listAncestries)
	router.HandleFunc("/ancestries/{name}", getAncestry)
	log.Fatal(http.ListenAndServe(":8080", router))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Pathfinder 2e API!\nAll data comes directly from Archives of Nethys\n%s", r.URL.Path[1:])
}

func listAncestries(w http.ResponseWriter, r *http.Request) {
	allAncestries := ancestries.GetAll()
	json.NewEncoder(w).Encode(allAncestries)
}

func getAncestry(w http.ResponseWriter, r *http.Request) {
	name := mux.Vars(r)["name"]
	ancestry, err := ancestries.GetByName(name)
	if err != nil {
		fmt.Fprintf(w, "%s! (%s) this should be a 404 message", err.Error(), name)
	} else {
		json.NewEncoder(w).Encode(ancestry)
	}
}
