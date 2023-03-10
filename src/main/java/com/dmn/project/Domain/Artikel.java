package com.dmn.project.Domain;

import jakarta.persistence.*;

@Entity
public class Artikel {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String naam;
    private String titel;
    private String inhoud;

    @ManyToOne
    private Wetboek wetboek;

    public Artikel(Long id, String naam, String titel, String inhoud, Wetboek wetboek) {
        this.id = id;
        this.naam = naam;
        this.titel = titel;
        this.inhoud = inhoud;
        this.wetboek = wetboek;
    }

    public Artikel() {
    }
}
