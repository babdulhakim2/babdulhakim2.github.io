---
layout: default
title: Creating Agent Dialogues
permalink: /ia/agent-dialogues/
---

# Creating Agent Dialogues

## Overview

This activity demonstrates how to create an agent dialogue using KQML (Knowledge Query and Manipulation Language) and KIF (Knowledge Interchange Format) between two agents: Alice (a procurement agent) and Bob (a warehouse stock management agent).

## Scenario

Alice is an agent designed to procure stock for a retail electronics store. Bob is an agent that controls the stock levels for a warehouse. In this dialogue, Alice needs to:

1. Query Bob about the available stock of 50-inch televisions
2. Ask about the number of HDMI slots these televisions have

## Agent Dialogue Implementation

### Initial Stock Query

```
; Alice asks Bob about available 50-inch TV stock
(ask-one
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology electronics-inventory
  :content (available-stock (product-type television)
                           (screen-size 50))
  :reply-with query-tv-stock-1)

; Bob responds with the available stock information
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology electronics-inventory
  :content (= (available-stock (product-type television)
                              (screen-size 50))
              15)
  :in-reply-to query-tv-stock-1)
```

### HDMI Ports Query

```
; Alice asks about the HDMI ports on the 50-inch TVs
(ask-one
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology electronics-inventory
  :content (product-feature (product-type television)
                           (screen-size 50)
                           (feature-type hdmi-ports))
  :reply-with query-tv-hdmi-1)

; Bob responds with the HDMI port information
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology electronics-inventory
  :content (= (product-feature (product-type television)
                              (screen-size 50)
                              (feature-type hdmi-ports))
              4)
  :in-reply-to query-tv-hdmi-1)
```

### Specific Model Query

```
; Alice asks for specific models of 50-inch TVs with 4 HDMI ports
(ask-all
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology electronics-inventory
  :content (and (product (type television)
                        (screen-size 50)
                        (hdmi-ports 4))
                (available-stock ?product ?quantity)
                (> ?quantity 0))
  :reply-with query-tv-models-1)

; Bob responds with a list of available models
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology electronics-inventory
  :content (and (product (id "SONY-X85J-50")
                        (type television)
                        (manufacturer "Sony")
                        (model "X85J")
                        (screen-size 50)
                        (hdmi-ports 4))
                (= (available-stock "SONY-X85J-50") 8)

                (product (id "LG-NANO75-50")
                        (type television)
                        (manufacturer "LG")
                        (model "NANO75")
                        (screen-size 50)
                        (hdmi-ports 4))
                (= (available-stock "LG-NANO75-50") 5)

                (product (id "SAMSUNG-Q60A-50")
                        (type television)
                        (manufacturer "Samsung")
                        (model "Q60A")
                        (screen-size 50)
                        (hdmi-ports 4))
                (= (available-stock "SAMSUNG-Q60A-50") 2))
  :in-reply-to query-tv-models-1)
```

### Purchase Request

```
; Alice requests to reserve 3 units of the Sony TV model
(achieve
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology electronics-inventory
  :content (reserve-stock (product-id "SONY-X85J-50")
                         (quantity 3))
  :reply-with reserve-sony-1)

; Bob confirms the reservation
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology electronics-inventory
  :content (reserved (product-id "SONY-X85J-50")
                    (quantity 3)
                    (reservation-id "RES-20250615-001")
                    (expiry "2025-06-22T23:59:59"))
  :in-reply-to reserve-sony-1)
```

## Analysis of the Dialogue

This dialogue demonstrates several key aspects of KQML/KIF-based agent communication:

1. **Performatives**: The use of different KQML performatives (`ask-one`, `ask-all`, `tell`, `achieve`) to express different communicative intentions.

2. **Message Parameters**: Each message includes parameters that provide context:

   - `:sender` and `:receiver` establish the communication participants
   - `:language` specifies KIF as the content language
   - `:ontology` references a shared knowledge model (electronics-inventory)
   - `:content` contains the actual KIF expressions
   - `:reply-with` and `:in-reply-to` create conversation threads

3. **Knowledge Representation**: The KIF content uses predicate logic to represent:

   - Product types and attributes (television, screen size, HDMI ports)
   - Stock levels and availability
   - Reservation details and constraints

4. **Conversation Flow**: The dialogue progresses logically from information gathering to action:
   - Initial stock availability query
   - Feature specification query
   - Detailed product information request
   - Transaction request and confirmation

This implementation enables Alice and Bob to communicate effectively despite potentially different internal architectures, demonstrating the power of standardized agent communication languages for facilitating interoperability in multi-agent systems.

---

[back to Unit 6 summary](../../ia/unit6-summary/) | [back to IA module](../../ia/)
