import json

with open('output/effective_balance_block.json', 'r') as file:
    effective_balance_block = json.load(file)
    assert effective_balance_block["9871487"] == 3.429832e+16
    assert effective_balance_block["9771487"] == 3.4088338e+16
    assert effective_balance_block["9671487"] == 3.404595e+16
    assert effective_balance_block["9571487"] == 3.3610768e+16
    assert effective_balance_block["9471487"] == 3.3255063e+16
    assert effective_balance_block["9371487"] == 3.3286509e+16
    assert effective_balance_block["9271487"] == 3.2926618e+16
    assert effective_balance_block["9171487"] == 3.2428959e+16
    assert effective_balance_block["9071487"] == 3.2569021e+16
    assert effective_balance_block["8971487"] == 3.2553593e+16
    assert effective_balance_block["8871487"] == 3.2428433e+16
    assert effective_balance_block["8771487"] == 3.2006237e+16
    assert effective_balance_block["8671487"] == 3.1602119e+16
    assert effective_balance_block["8571487"] == 3.1552848e+16
    assert effective_balance_block["8471487"] == 3.0875961e+16
    assert effective_balance_block["8371487"] == 2.9889968e+16
    assert effective_balance_block["8271487"] == 2.9186053e+16
    assert effective_balance_block["8171487"] == 2.9106549e+16
    assert effective_balance_block["8071487"] == 2.8724682e+16
    assert effective_balance_block["7971487"] == 2.8666282e+16 
                                            
with open('output/balance_block.json', 'r') as file:
    balance_block = json.load(file)
    assert balance_block["9871487"] == 3.43612521e+16
    assert balance_block["9771487"] == 3.415120892e+16
    assert balance_block["9671487"] == 3.410851391e+16
    assert balance_block["9571487"] == 3.367295454e+16
    assert balance_block["9471487"] == 3.331732792e+16
    assert balance_block["9371487"] == 3.334996486e+16
    assert balance_block["9271487"] == 3.298925684e+16
    assert balance_block["9171487"] == 3.249237626e+16
    assert balance_block["9071487"] == 3.263177398e+16
    assert balance_block["8971487"] == 3.261594218e+16
    assert balance_block["8871487"] == 3.249144871e+16
    assert balance_block["8771487"] == 3.206928212e+16
    assert balance_block["8671487"] == 3.1666731e+16
    assert balance_block["8571487"] == 3.16185922e+16
    assert balance_block["8471487"] == 3.094362384e+16
    assert balance_block["8371487"] == 2.996068731e+16
    assert balance_block["8271487"] == 2.9256614e+16
    assert balance_block["8171487"] == 2.917796431e+16
    assert balance_block["8071487"] == 2.879712568e+16
    assert balance_block["7971487"] == 2.874599525e+16


with open('output/slashed_block.json', 'r') as file:
    slashed = json.load(file)
    assert slashed["9871487"] == 438
    assert slashed["9771487"] == 438
    assert slashed["9671487"] == 438
    assert slashed["9571487"] == 437
    assert slashed["9471487"] == 437
    assert slashed["9371487"] == 435
    assert slashed["9271487"] == 433
    assert slashed["9171487"] == 431
    assert slashed["9071487"] == 431
    assert slashed["8971487"] == 431
    assert slashed["8871487"] == 431
    assert slashed["8771487"] == 425
    assert slashed["8671487"] == 425
    assert slashed["8571487"] == 423
    assert slashed["8471487"] == 417
    assert slashed["8371487"] == 413
    assert slashed["8271487"] == 411
    assert slashed["8171487"] == 407
    assert slashed["8071487"] == 405
    assert slashed["7971487"] == 405

with open('output/status_block.json', 'r') as file:
    status = json.load(file)
    assert status["9471487"]["active_ongoing"] == 1027537
    assert status["9471487"]["pending_initialized"] == 122
    assert status["9471487"]["withdrawal_done"] == 439708
    assert status["9471487"]["exited_unslashed"] == 1232
    assert status["9471487"]["withdrawal_possible"] == 9981
    assert status["9471487"]["exited_slashed"] == 6
    assert status["9471487"]["active_exiting"] == 18
    assert status["9471487"]["pending_queued"] == 455

    assert status["9371487"]["withdrawal_possible"] == 7203
    assert status["9371487"]["exited_slashed"] == 4
    assert status["9371487"]["active_exiting"] == 60
    assert status["9371487"]["pending_queued"] == 3409
    assert status["9371487"]["active_ongoing"] == 1027269
    assert status["9371487"]["pending_initialized"] == 170
    assert status["9371487"]["withdrawal_done"] == 420455
    assert status["9371487"]["exited_unslashed"] == 2265

    assert status["9071487"]["withdrawal_done"] == 374124
    assert status["9071487"]["exited_unslashed"] == 2050
    assert status["9071487"]["exited_slashed"] == 1
    assert status["9071487"]["active_ongoing"] == 1013960
    assert status["9071487"]["pending_initialized"] == 364
    assert status["9071487"]["active_exiting"] == 1
    assert status["9071487"]["withdrawal_possible"] == 1770

    assert status["8871487"]["active_exiting"] == 41
    assert status["8871487"]["pending_queued"] == 21973
    assert status["8871487"]["exited_slashed"] == 8
    assert status["8871487"]["withdrawal_possible"] == 5234
    assert status["8871487"]["withdrawal_done"] == 352601
    assert status["8871487"]["exited_unslashed"] == 1875
    assert status["8871487"]["active_ongoing"] == 984262
    assert status["8871487"]["pending_initialized"] == 228

    assert status["8571487"]["withdrawal_possible"] == 4911
    assert status["8571487"]["exited_slashed"] == 11
    assert status["8571487"]["active_exiting"] == 9
    assert status["8571487"]["active_ongoing"] == 978782
    assert status["8571487"]["pending_initialized"] == 79
    assert status["8571487"]["withdrawal_done"] == 281948
    assert status["8571487"]["exited_unslashed"] == 2323

    assert status["8371487"]["active_ongoing"] == 926515
    assert status["8371487"]["pending_initialized"] == 935
    assert status["8371487"]["withdrawal_done"] == 253352
    assert status["8371487"]["exited_unslashed"] == 1232
    assert status["8371487"]["withdrawal_possible"] == 4123
    assert status["8371487"]["exited_slashed"] == 8
    assert status["8371487"]["active_exiting"] == 10
    assert status["8371487"]["pending_queued"] == 2156

    assert status["8071487"]["active_ongoing"] == 894701
    assert status["8071487"]["pending_initialized"] == 474
    assert status["8071487"]["withdrawal_done"] == 199414
    assert status["8071487"]["exited_unslashed"] == 1048
    assert status["8071487"]["withdrawal_possible"] == 1854
    assert status["8071487"]["exited_slashed"] == 6
    assert status["8071487"]["active_exiting"] == 31

    assert status["9671487"]["active_exiting"] == 96
    assert status["9671487"]["pending_queued"] == 2714
    assert status["9671487"]["exited_slashed"] == 2
    assert status["9671487"]["withdrawal_possible"] == 3741
    assert status["9671487"]["withdrawal_done"] == 464874
    assert status["9671487"]["exited_unslashed"] == 2499
    assert status["9671487"]["active_ongoing"] == 1054890
    assert status["9671487"]["pending_initialized"] == 191

    assert status["9171487"]["active_exiting"] == 1054
    assert status["9171487"]["withdrawal_possible"] == 4270
    assert status["9171487"]["withdrawal_done"] == 394947
    assert status["9171487"]["exited_unslashed"] == 1603
    assert status["9171487"]["active_ongoing"] == 1006483
    assert status["9171487"]["pending_initialized"] == 200

    assert status["8171487"]["active_ongoing"] == 891980
    assert status["8171487"]["pending_initialized"] == 297
    assert status["8171487"]["withdrawal_done"] == 211317
    assert status["8171487"]["exited_unslashed"] == 3328
    assert status["8171487"]["withdrawal_possible"] == 8574
    assert status["8171487"]["active_slashed"] == 2
    assert status["8171487"]["active_exiting"] == 5040
    assert status["8171487"]["pending_queued"] == 655

    assert status["8971487"]["exited_slashed"] == 6
    assert status["8971487"]["withdrawal_possible"] == 2237
    assert status["8971487"]["withdrawal_done"] == 364367
    assert status["8971487"]["exited_unslashed"] == 1723
    assert status["8971487"]["active_exiting"] == 24
    assert status["8971487"]["pending_queued"] == 12628
    assert status["8971487"]["active_ongoing"] == 1000664
    assert status["8971487"]["pending_initialized"] == 938

    assert status["8771487"]["exited_slashed"] == 4
    assert status["8771487"]["withdrawal_possible"] == 4974
    assert status["8771487"]["withdrawal_done"] == 332937
    assert status["8771487"]["exited_unslashed"] == 3294
    assert status["8771487"]["pending_queued"] == 14102
    assert status["8771487"]["active_ongoing"] == 977812
    assert status["8771487"]["pending_initialized"] == 648

    assert status["7971487"]["active_exiting"] == 1
    assert status["7971487"]["exited_slashed"] == 106
    assert status["7971487"]["withdrawal_possible"] == 5463
    assert status["7971487"]["withdrawal_done"] == 178721
    assert status["7971487"]["exited_unslashed"] == 1253
    assert status["7971487"]["active_ongoing"] == 889011
    assert status["7971487"]["pending_initialized"] == 92

    assert status["9571487"]["active_exiting"] == 13
    assert status["9571487"]["pending_queued"] == 5226
    assert status["9571487"]["exited_slashed"] == 3
    assert status["9571487"]["withdrawal_possible"] == 2463
    assert status["9571487"]["withdrawal_done"] == 455983
    assert status["9571487"]["exited_unslashed"] == 477
    assert status["9571487"]["active_ongoing"] == 1042163
    assert status["9571487"]["pending_initialized"] == 113

    assert status["9871487"]["withdrawal_possible"] == 3242
    assert status["9871487"]["withdrawal_done"] == 493118
    assert status["9871487"]["exited_unslashed"] == 222
    assert status["9871487"]["pending_queued"] == 911
    assert status["9871487"]["active_exiting"] == 2
    assert status["9871487"]["active_ongoing"] == 1067458
    assert status["9871487"]["pending_initialized"] == 86

    assert status["9271487"]["active_ongoing"] == 1019913
    assert status["9271487"]["pending_initialized"] == 3374
    assert status["9271487"]["active_exiting"] == 109
    assert status["9271487"]["pending_queued"] == 3668
    assert status["9271487"]["withdrawal_done"] == 407061
    assert status["9271487"]["exited_unslashed"] == 1245
    assert status["9271487"]["exited_slashed"] == 2
    assert status["9271487"]["withdrawal_possible"] == 3926

    assert status["8671487"]["withdrawal_done"] == 309494
    assert status["8671487"]["exited_unslashed"] == 1927
    assert status["8671487"]["withdrawal_possible"] == 5355
    assert status["8671487"]["active_ongoing"] == 977095
    assert status["8671487"]["pending_initialized"] == 104
    assert status["8671487"]["pending_queued"] == 3048
    assert status["8671487"]["active_exiting"] == 138
    assert status["8671487"]["exited_slashed"] == 12

    assert status["8271487"]["active_ongoing"] == 903816
    assert status["8271487"]["pending_initialized"] == 468
    assert status["8271487"]["active_exiting"] == 867
    assert status["8271487"]["pending_queued"] == 1297
    assert status["8271487"]["withdrawal_done"] == 235091
    assert status["8271487"]["exited_unslashed"] == 2500
    assert status["8271487"]["exited_slashed"] == 6
    assert status["8271487"]["withdrawal_possible"] == 3575

    assert status["9771487"]["active_exiting"] == 565
    assert status["9771487"]["active_ongoing"] == 1062332
    assert status["9771487"]["pending_initialized"] == 22
    assert status["9771487"]["withdrawal_possible"] == 2000
    assert status["9771487"]["exited_slashed"] == 1
    assert status["9771487"]["withdrawal_done"] == 481235
    assert status["9771487"]["exited_unslashed"] == 374

    assert status["8471487"]["pending_queued"] == 4128
    assert status["8471487"]["active_ongoing"] == 957080
    assert status["8471487"]["pending_initialized"] == 403
    assert status["8471487"]["withdrawal_possible"] == 2866
    assert status["8471487"]["exited_slashed"] == 10
    assert status["8471487"]["withdrawal_done"] == 268245
    assert status["8471487"]["exited_unslashed"] == 789


with open('output/effective_balance_total.json', 'r') as file:
    effective_balance_total = json.load(file)
    assert effective_balance_total['effective_balance'] == 6.37102271e+17

with open('output/balance_total.json', 'r') as file:
    balance_total = json.load(file)
    assert balance_total['balance'] == 6.384186359e+17

with open('output/slashed_total.json', 'r') as file:
    slashed_total = json.load(file)
    assert slashed_total['slashed'] == 8511

with open('output/status_total.json', 'r') as file:
    status_total = json.load(file)
    assert status_total["withdrawal_done"] == 6918992
    assert status_total["active_slashed"] == 2
    assert status_total["exited_unslashed"] == 33259
    assert status_total["active_ongoing"] == 19703723
    assert status_total["active_exiting"] == 8079
    assert status_total["pending_queued"] == 76370
    assert status_total["withdrawal_possible"] == 87762
    assert status_total["pending_initialized"] == 9308
    assert status_total["exited_slashed"] == 196

