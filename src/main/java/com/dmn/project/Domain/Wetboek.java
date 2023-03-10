package com.dmn.project.Domain;

import jakarta.persistence.*;

import java.util.List;

@Entity
public class Wetboek {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String naam;
    private String beschrijving;

    @OneToMany
    private List<Artikel> Atrikelen;

    public Wetboek(Long id, String naam, String beschrijving, List<Artikel> atrikelen) {
        this.id = id;
        this.naam = naam;
        this.beschrijving = beschrijving;
        Atrikelen = atrikelen;
    }

    public Wetboek() {
    }
}
