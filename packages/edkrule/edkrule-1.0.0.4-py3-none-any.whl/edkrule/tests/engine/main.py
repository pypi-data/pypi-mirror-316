from edkrule.edk_rule import EdkRule

if __name__ == '__main__':
    # string = """
    # getSubjectArmCode==\"Arm A: ONC-392 + LU 177 VIPIVOTIDE\" || getSubjectArmCode==\"Arm 1: ONC-392 LOW DOSE + LU 177 VIPIVOTIDE\" || getSubjectArmCode==\"Arm 2: ONC-392 HIGH DOSE + LU 177 VIPIVOTIDE\"
    # """
    # string = """toDate($C1D1.ONC-392 Administration.ECSTDAT)!=""&& toDate($*.*.LBDAT)!=""&& toDate("2015-1-12 "+$C1D1.ONC-392 Administration.ECSTTIM+":00")!="" &&toDate("2015-1-12 "+$*.*.*+":00")!=""?dateDiff($C1D1.ONC-392 Administration.ECSTDAT+" "+$C1D1.ONC-392 Administration.ECSTTIM+":00",$*.*.LBDAT+" "+$*.*.*+":00","m")>0:true"""
    # string = """autoValue(RoundN(sum(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLLONG, $*.Target Lesions Assessment (Details) (Screening).TLLOC != 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU == "MM"),1/10) , getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "CM") , multiply(getSumOfItemInLog($*.Target Lesions Assessment (Details) (Screening).TLSHORT, $*.Target Lesions Assessment (Details) (Screening).TLLOC == 11 && $*.Target Lesions Assessment (Details) (Screening).TLDIAU== "MM"),1/10)), 0.01), true)"""
    # string = """mustAnswer($*.*.CRONGO)&&$*.*.CRONGO=='N'?$*.*.*!='':true"""
    # exp = EdkRule.expression(string)
    # exp.tree_data()
    # string = """a==1&&b==1?true:false"""
    # string = """a&&b==1?x==1?true:false:false"""
    # string = """a&&b==1?x==1?true:false:y==1?true:false"""
    # string = """a==1||b==2||c==3"""
    string = """a==1&&b==2||c"""
    # string = """a||b==2||c==2"""
    # string = """a||(b==2||c==2)"""
    # string = """max=a>b?a:b"""

    EdkRule.draw(string, "rule.html")