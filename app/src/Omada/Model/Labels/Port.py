value_map: dict[str, dict] = {
    "linkStatus": {
        0: "Down",
        1: "Up"
    },
    "linkSpeed": {
        -1: "Down",
        0: "Auto",
        1: "10M",
        2: "100M",
        3: "1000M",
        4: "2500M",
        5: "10G",
        6: "5G",
    },
    "duplex": {
        -1: "Down",
        0: "Auto",
        1: "Half",
        2: "Full",
    },
    "mirrorMode": {
        0: "ingress",
        1: "egress",
        2: "ingress and egress",
    },
}
