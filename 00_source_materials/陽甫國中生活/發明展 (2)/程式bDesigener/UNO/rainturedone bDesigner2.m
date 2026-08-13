<xml xmlns="http://www.w3.org/1999/xhtml">
  <variables>
    <variable type="" id="36q*i(PZk]9GjQ;MqWj3">計時a</variable>
    <variable type="" id="P`-XV^yY])h{C~h^=bkz">距離</variable>
    <variable type="" id="I`%LRZ;y=yaFJowBO:aq">計時b</variable>
  </variables>
  <comment id="E[h?jIybHu^[ogp47Hrh" x="646" y="132" h="120" w="160">130開
50關
  
  </comment>
  <block type="variables_set" id="dMsv!2-2tqXM]iSrDD^;" x="162" y="-88">
    <field name="VALUE1">int</field>
    <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
    <value name="VALUE">
      <block type="math_number" id="^*mCp^jT%2Of`ePY:V+5">
        <field name="NUM">0</field>
      </block>
    </value>
    <next>
      <block type="variables_set" id="0A7K`EFF2j@Is:(.]Jy]">
        <field name="VALUE1">int</field>
        <field name="VAR" id="I`%LRZ;y=yaFJowBO:aq" variabletype="">計時b</field>
        <value name="VALUE">
          <block type="math_number" id="sqEn@+H3!dy|fBEcBZBM">
            <field name="NUM">0</field>
          </block>
        </value>
        <next>
          <block type="variables_set" id="7E08(WK3*]/~-$]o~6Yo">
            <field name="VALUE1">int</field>
            <field name="VAR" id="P`-XV^yY])h{C~h^=bkz" variabletype="">距離</field>
            <value name="VALUE">
              <block type="math_number" id="A+Ca$lbf1aX~bwPW)FZw">
                <field name="NUM">0</field>
              </block>
            </value>
            <next>
              <block type="start" id="dW.]YFCvf@z^SGNFSUFz">
                <statement name="setup">
                  <block type="servosetup1" id="d8c78EIvPE8FDSFtQDGv">
                    <value name="pin">
                      <shadow type="math_number" id="QkP`mii;bR$jd`-|esnL">
                        <field name="NUM">1</field>
                      </shadow>
                    </value>
                    <value name="value">
                      <shadow type="math_number" id="eOVoi4kOQ`!p,NSo{#LB">
                        <field name="NUM">12</field>
                      </shadow>
                    </value>
                    <value name="value1">
                      <shadow type="math_number" id="yfX[lAxe|6+^Q0AR-(Bo">
                        <field name="NUM">544</field>
                      </shadow>
                    </value>
                    <value name="value2">
                      <shadow type="math_number" id="#iquUH+H`?{.Yew^mC?.">
                        <field name="NUM">2400</field>
                      </shadow>
                    </value>
                    <next>
                      <block type="servosetup" id="JjQJMV8S[L$7!S#0*5YI">
                        <value name="pin">
                          <shadow type="math_number" id="KVkFnvF2w[@9|{w-@{.U">
                            <field name="NUM">1</field>
                          </shadow>
                        </value>
                        <value name="value">
                          <shadow type="math_number" id="o{V{i.B[!}VsAcEX@bm?">
                            <field name="NUM">12</field>
                          </shadow>
                        </value>
                        <next>
                          <block type="servowrite" id="PMtYhiPks8NuHT;uNF,w">
                            <value name="pin">
                              <shadow type="math_number" id="=5vdK,!J|zj4a[]sx}8R">
                                <field name="NUM">1</field>
                              </shadow>
                            </value>
                            <value name="value">
                              <shadow type="math_number" id="~P1g:qZ;YIgQ?]TJ2mmp">
                                <field name="NUM">90</field>
                              </shadow>
                            </value>
                          </block>
                        </next>
                      </block>
                    </next>
                  </block>
                </statement>
                <statement name="loop">
                  <block type="serial_write" id="PD(RUQ8h8Gswp=EE]Y]%">
                    <value name="value">
                      <shadow type="text" id="K8c~xp(}p;|4RDS6UQS7">
                        <field name="TEXT">Hello</field>
                      </shadow>
                      <block type="text_join" id="Do^ZW}L+S{^$WHmpRa?J">
                        <mutation items="4"></mutation>
                        <value name="ADD0">
                          <block type="variables_get" id="r(Jk:ROIX^MN%YH-%hBu">
                            <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                          </block>
                        </value>
                        <value name="ADD1">
                          <block type="text" id="je!^+@M2sC~pv|{i|qYg">
                            <field name="TEXT">，</field>
                          </block>
                        </value>
                        <value name="ADD2">
                          <block type="variables_get" id="]~9x#hJ^0NY^,Yh@v#p[">
                            <field name="VAR" id="I`%LRZ;y=yaFJowBO:aq" variabletype="">計時b</field>
                          </block>
                        </value>
                        <value name="ADD3">
                          <block type="text" id="pZ:8j5NsQzLnx:I3nxf-">
                            <field name="TEXT">;</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <next>
                      <block type="serial_write1" id="E~;B$Bv6Ab@T*]$6S5hG">
                        <value name="value">
                          <shadow type="text" id="#$vlb,{/Z`JAL|g/wkQI">
                            <field name="TEXT">Hello</field>
                          </shadow>
                          <block type="dht11temp" id=".{9A#h-14Ywg@K9X[n+2">
                            <value name="NAME">
                              <shadow type="math_number" id="):4aM1aIK_MiSdhykWV5">
                                <field name="NUM">16</field>
                              </shadow>
                            </value>
                          </block>
                        </value>
                        <next>
                          <block type="controls_if" id="f82VRO@O^tVJ2_I|6b;T">
                            <value name="IF0">
                              <shadow type="logic_boolean" id="T!!0.*BOy~C{:q@MId/c">
                                <field name="BOOL">TRUE</field>
                              </shadow>
                              <block type="logic_compare" id="7-7Noir!h~]--nRgs8Tf">
                                <field name="OP">GT</field>
                                <value name="A">
                                  <block type="digital2" id="^KVP9y3vVuWabPM7E`+r">
                                    <value name="pin">
                                      <shadow type="math_number" id="Ii,|%^US4-`nzs91oBG3">
                                        <field name="NUM">14</field>
                                      </shadow>
                                    </value>
                                  </block>
                                </value>
                                <value name="B">
                                  <block type="math_number" id="l$yg+kq$Hh?Q7Kpjfd+B">
                                    <field name="NUM">1000</field>
                                  </block>
                                </value>
                              </block>
                            </value>
                            <statement name="DO0">
                              <block type="servowrite" id="}:YYjjeh^[_!/2JYhk%C">
                                <value name="pin">
                                  <shadow type="math_number" id="ry;@[e;k;fAR}+}qd0|,">
                                    <field name="NUM">1</field>
                                  </shadow>
                                </value>
                                <value name="value">
                                  <shadow type="math_number" id="5uRQ|8T(Z_N^9KZ{{Icp">
                                    <field name="NUM">50</field>
                                  </shadow>
                                </value>
                              </block>
                            </statement>
                            <next>
                              <block type="controls_if" id="w~^5WJT`%9dYVYJ/X|uW">
                                <value name="IF0">
                                  <shadow type="logic_boolean" id="T!!0.*BOy~C{:q@MId/c">
                                    <field name="BOOL">TRUE</field>
                                  </shadow>
                                  <block type="logic_compare" id="U-%PR!ZFF|_yo/`t6pB^">
                                    <field name="OP">LT</field>
                                    <value name="A">
                                      <block type="digital2" id="k[-l6LgMwA8;jYh8!BnQ">
                                        <value name="pin">
                                          <shadow type="math_number" id="T5#[/j,_QP9u;dUvWhVN">
                                            <field name="NUM">14</field>
                                          </shadow>
                                        </value>
                                      </block>
                                    </value>
                                    <value name="B">
                                      <block type="math_number" id="vBDxeiYxMky,jA}laj2[">
                                        <field name="NUM">1000</field>
                                      </block>
                                    </value>
                                  </block>
                                </value>
                                <statement name="DO0">
                                  <block type="servowrite" id="N1UV;S-Y].Y6ZR[@e92Q">
                                    <value name="pin">
                                      <shadow type="math_number" id=";]YyldL]91DwL%bmLgB#">
                                        <field name="NUM">1</field>
                                      </shadow>
                                    </value>
                                    <value name="value">
                                      <shadow type="math_number" id="N0@:J8Ek0.Tg.1Io)|!(">
                                        <field name="NUM">130</field>
                                      </shadow>
                                    </value>
                                  </block>
                                </statement>
                                <next>
                                  <block type="controls_if" id="{/~Uqb5_UJc83=~Av:vs">
                                    <value name="IF0">
                                      <shadow type="logic_boolean" id="~!bZAFgm=%}ws3E`vjR2">
                                        <field name="BOOL">TRUE</field>
                                      </shadow>
                                      <block type="logic_compare" id="[s:hPERdGZ=K,]zgN:_F">
                                        <field name="OP">GT</field>
                                        <value name="A">
                                          <block type="dht11temp" id="oftxL#%|1M#EG/Yr[AAt">
                                            <value name="NAME">
                                              <shadow type="math_number" id="q-/4M2[zu|nv!^s;9G3S">
                                                <field name="NUM">16</field>
                                              </shadow>
                                            </value>
                                          </block>
                                        </value>
                                        <value name="B">
                                          <block type="math_number" id="-LL*8t[vtUDQngl7Wjw_">
                                            <field name="NUM">33</field>
                                          </block>
                                        </value>
                                      </block>
                                    </value>
                                    <statement name="DO0">
                                      <block type="servowrite" id="^fAn^MJQL#}!;JpBP:9?">
                                        <value name="pin">
                                          <shadow type="math_number" id="d$s}cVAzg4zLA71EdB;@">
                                            <field name="NUM">1</field>
                                          </shadow>
                                        </value>
                                        <value name="value">
                                          <shadow type="math_number" id="Ey3!J`Xs#b|@8z$7Yx{t">
                                            <field name="NUM">130</field>
                                          </shadow>
                                        </value>
                                        <next>
                                          <block type="digital1" id="vf3Xv$]N.Mx;}mY9%UiX">
                                            <value name="pin">
                                              <shadow type="math_number" id=")MLKJ@nXObD#%;yD-m74">
                                                <field name="NUM">17</field>
                                              </shadow>
                                            </value>
                                            <value name="value">
                                              <shadow type="math_number" id=";=m)^y7yRIWB%m+odSiQ">
                                                <field name="NUM">1</field>
                                              </shadow>
                                            </value>
                                          </block>
                                        </next>
                                      </block>
                                    </statement>
                                    <next>
                                      <block type="controls_if" id="c`C.Q%`8pfY*!Pt#m$E1">
                                        <value name="IF0">
                                          <shadow type="logic_boolean" id="Jp#`C09L`YWChN]cTka8">
                                            <field name="BOOL">TRUE</field>
                                          </shadow>
                                          <block type="logic_compare" id="l=1NsaFs`0NXaX?X$kWL">
                                            <field name="OP">EQ</field>
                                            <value name="A">
                                              <block type="digital2" id="+x3-3eka$rf*K=#8%a,2">
                                                <value name="pin">
                                                  <shadow type="math_number" id="7dR}3eRz]F=,R*`3E96q">
                                                    <field name="NUM">17</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </value>
                                            <value name="B">
                                              <block type="math_number" id="ls~7ZelxWI=G7h!,X;)/">
                                                <field name="NUM">1</field>
                                              </block>
                                            </value>
                                          </block>
                                        </value>
                                        <statement name="DO0">
                                          <block type="math_change" id="$8/QAf#h%[M9}HzzW}pJ">
                                            <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                            <value name="DELTA">
                                              <shadow type="math_number" id="yBkmZ{q9rzaZY02uh1D$">
                                                <field name="NUM">1</field>
                                              </shadow>
                                              <block type="math_arithmetic" id="O-!)fe[hXv!|gqPL^?kr">
                                                <field name="OP">ADD</field>
                                                <value name="A">
                                                  <shadow type="math_number" id="k2S3Yw6V*N@]jm5^vtM}">
                                                    <field name="NUM">1</field>
                                                  </shadow>
                                                  <block type="variables_get" id="LM}k$cgfZv$KIPkT33;)">
                                                    <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                                  </block>
                                                </value>
                                                <value name="B">
                                                  <shadow type="math_number" id=".]I8LooV7vJg;sgL~;Z7">
                                                    <field name="NUM">1</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </value>
                                            <next>
                                              <block type="arduinodelay" id="q?eDO}#Rdyu]kb3Oh^o,">
                                                <value name="value">
                                                  <shadow type="math_number" id="MC@${D/t%$i^paJhHavV">
                                                    <field name="NUM">500</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </next>
                                          </block>
                                        </statement>
                                        <next>
                                          <block type="controls_if" id="$Ap05JV)`lW3GX@*y:3u">
                                            <value name="IF0">
                                              <shadow type="logic_boolean" id="zoF2fe_c(bnk1q@go(jE">
                                                <field name="BOOL">TRUE</field>
                                              </shadow>
                                              <block type="logic_compare" id="0,z0WR+Eb--}=4_Q6BaE">
                                                <field name="OP">GT</field>
                                                <value name="A">
                                                  <block type="variables_get" id="PHcyt}xm90d*Gvsc)1X(">
                                                    <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                                  </block>
                                                </value>
                                                <value name="B">
                                                  <block type="math_number" id="DKDZf}o]u2?M`Sqpv2eQ">
                                                    <field name="NUM">10</field>
                                                  </block>
                                                </value>
                                              </block>
                                            </value>
                                            <statement name="DO0">
                                              <block type="digital1" id="W)tAe4L(XyO;k^|)6|`X">
                                                <value name="pin">
                                                  <shadow type="math_number" id="WUnimn7`fjoNZ^1,P?:W">
                                                    <field name="NUM">17</field>
                                                  </shadow>
                                                </value>
                                                <value name="value">
                                                  <shadow type="math_number" id="@,TfPX4g-RY~dk4]V8w$">
                                                    <field name="NUM">0</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </statement>
                                            <next>
                                              <block type="controls_if" id="m1QNMZD}$LfW1FBk6y}@">
                                                <mutation else="1"></mutation>
                                                <value name="IF0">
                                                  <shadow type="logic_boolean" id="@Lv)03*sMXGN@2(D/{`X">
                                                    <field name="BOOL">TRUE</field>
                                                  </shadow>
                                                  <block type="logic_operation" id="}AjTP-=M)5,n/DG_gEF=">
                                                    <field name="OP">AND</field>
                                                    <value name="A">
                                                      <block type="logic_compare" id="Mp~~Y#151[N*j@cl_%Vw">
                                                        <field name="OP">LT</field>
                                                        <value name="A">
                                                          <block type="analog2" id="Ys*p]9eeNPnFhK?9XuxN">
                                                            <value name="pin">
                                                              <shadow type="math_number" id="0D$In%2+svdW75}SILP?">
                                                                <field name="NUM">15</field>
                                                              </shadow>
                                                            </value>
                                                          </block>
                                                        </value>
                                                        <value name="B">
                                                          <block type="math_number" id="Y+Md0!DlD$P.RIigR5xP">
                                                            <field name="NUM">650</field>
                                                          </block>
                                                        </value>
                                                      </block>
                                                    </value>
                                                    <value name="B">
                                                      <block type="logic_compare" id="eMdl?u3(Kc0X3nJ7`/;q">
                                                        <field name="OP">LT</field>
                                                        <value name="A">
                                                          <block type="variables_get" id="A7p|k12OCL=ge2lbt]j=">
                                                            <field name="VAR" id="P`-XV^yY])h{C~h^=bkz" variabletype="">距離</field>
                                                          </block>
                                                        </value>
                                                        <value name="B">
                                                          <block type="math_number" id="DbqEQTqKY$AGNXY#CgB+">
                                                            <field name="NUM">30</field>
                                                          </block>
                                                        </value>
                                                      </block>
                                                    </value>
                                                  </block>
                                                </value>
                                                <statement name="DO0">
                                                  <block type="controls_if" id="Hk^mEWv8/X:#kF+H:E$9">
                                                    <mutation else="1"></mutation>
                                                    <value name="IF0">
                                                      <shadow type="logic_boolean" id="|?^3_jUaZsP]+^N]K_HQ">
                                                        <field name="BOOL">TRUE</field>
                                                      </shadow>
                                                      <block type="logic_compare" id="|(4w677f.F(0^OAz;CcV">
                                                        <field name="OP">LT</field>
                                                        <value name="A">
                                                          <block type="variables_get" id=":;WZTalLD/T={obd#2?~">
                                                            <field name="VAR" id="I`%LRZ;y=yaFJowBO:aq" variabletype="">計時b</field>
                                                          </block>
                                                        </value>
                                                        <value name="B">
                                                          <block type="math_number" id="mogjJLiJ7K6?gioU7^-,">
                                                            <field name="NUM">20</field>
                                                          </block>
                                                        </value>
                                                      </block>
                                                    </value>
                                                    <statement name="DO0">
                                                      <block type="digital1" id="~})qy{^47R?MO`25pS[W">
                                                        <value name="pin">
                                                          <shadow type="math_number" id="C}ao*8$0Lv-A6kL2@k6G">
                                                            <field name="NUM">13</field>
                                                          </shadow>
                                                        </value>
                                                        <value name="value">
                                                          <shadow type="math_number" id=")dx*o,p_HZfbc,l_nG`K">
                                                            <field name="NUM">1</field>
                                                          </shadow>
                                                        </value>
                                                      </block>
                                                    </statement>
                                                    <statement name="ELSE">
                                                      <block type="digital1" id="`dnjJ5~eril2X;a7;==e">
                                                        <value name="pin">
                                                          <shadow type="math_number" id="^)`s2nyS]!:DI/Eu|7P8">
                                                            <field name="NUM">13</field>
                                                          </shadow>
                                                        </value>
                                                        <value name="value">
                                                          <shadow type="math_number" id="g9/9QlSOABdU-8[TiX+l">
                                                            <field name="NUM">0</field>
                                                          </shadow>
                                                        </value>
                                                      </block>
                                                    </statement>
                                                  </block>
                                                </statement>
                                                <statement name="ELSE">
                                                  <block type="digital1" id="=P[4P*Hp*DpFLq~T_Tc~">
                                                    <value name="pin">
                                                      <shadow type="math_number" id="Cz0Rrd%w3|7B)}[wV4K8">
                                                        <field name="NUM">13</field>
                                                      </shadow>
                                                    </value>
                                                    <value name="value">
                                                      <shadow type="math_number" id="ueL|OsxeGQkJx/(u1I+B">
                                                        <field name="NUM">0</field>
                                                      </shadow>
                                                    </value>
                                                    <next>
                                                      <block type="math_change" id="IwPe=xKOqj0;y6~lB~p3">
                                                        <field name="VAR" id="I`%LRZ;y=yaFJowBO:aq" variabletype="">計時b</field>
                                                        <value name="DELTA">
                                                          <shadow type="math_number" id="k(Dwx/c{*},@cp-|b3*E">
                                                            <field name="NUM">0</field>
                                                          </shadow>
                                                        </value>
                                                      </block>
                                                    </next>
                                                  </block>
                                                </statement>
                                                <next>
                                                  <block type="math_change" id="gbt2se=F_=ek=j(Y$ij$">
                                                    <field name="VAR" id="P`-XV^yY])h{C~h^=bkz" variabletype="">距離</field>
                                                    <value name="DELTA">
                                                      <shadow type="math_number" id=",q$vQB)6-3_Tfs2Hav;*">
                                                        <field name="NUM">1</field>
                                                      </shadow>
                                                      <block type="aultrasound" id="npDwVjmObcTH4fBejRzb">
                                                        <value name="pin">
                                                          <shadow type="math_number" id="~K.{rMj$,ZvCB/%,svz2">
                                                            <field name="NUM">2</field>
                                                          </shadow>
                                                        </value>
                                                        <value name="pin1">
                                                          <shadow type="math_number" id="Hm$X|~*^osy(=KU}?6!U">
                                                            <field name="NUM">3</field>
                                                          </shadow>
                                                        </value>
                                                      </block>
                                                    </value>
                                                  </block>
                                                </next>
                                              </block>
                                            </next>
                                          </block>
                                        </next>
                                      </block>
                                    </next>
                                  </block>
                                </next>
                              </block>
                            </next>
                          </block>
                        </next>
                      </block>
                    </next>
                  </block>
                </statement>
              </block>
            </next>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>