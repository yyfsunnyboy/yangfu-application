<xml xmlns="http://www.w3.org/1999/xhtml">
  <variables>
    <variable type="" id="36q*i(PZk]9GjQ;MqWj3">計時a</variable>
    <variable type="" id="!bo:M9uNNy?bl6VZt;mY">計時b</variable>
    <variable type="" id="FO?PC{-AlDoW3(yAQ!y]">距離</variable>
  </variables>
  <comment id="4k^a2bjiFCrdh*C7E-v9" x="886" y="-60" h="120" w="160">130開
50關
  </comment>
  <block type="variables_set" id="H:f1Y]YkrK*Adw@d~vOp" x="-13" y="-137">
    <field name="VALUE1">int</field>
    <field name="VAR" id="FO?PC{-AlDoW3(yAQ!y]" variabletype="">距離</field>
    <value name="VALUE">
      <block type="math_number" id="hAaV=w.a,*xH/YF6yqbo">
        <field name="NUM">0</field>
      </block>
    </value>
    <next>
      <block type="variables_set" id=";A`}|j)Czqvp!}(bq?~k">
        <field name="VALUE1">int</field>
        <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
        <value name="VALUE">
          <block type="math_number" id="_rstaHa3r5Pu5ejcH6P#">
            <field name="NUM">0</field>
          </block>
        </value>
        <next>
          <block type="variables_set" id="M%R4I-}Qg#`0Q,(mSwc|">
            <field name="VALUE1">int</field>
            <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
            <value name="VALUE">
              <block type="math_number" id="Ic.Lv_u4:|0)O$6zcoD@">
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
                          <block type="variables_get" id="n`dEl.M%tRFG9C5/2sk4">
                            <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                          </block>
                        </value>
                        <value name="ADD3">
                          <block type="text" id="!|JE[[dioAOYosVI/9v=">
                            <field name="TEXT">;</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <next>
                      <block type="serial_write" id="$e~|]EM[ALz;S1bJLfr-">
                        <value name="value">
                          <shadow type="text" id="cA|j_OGq=MSqKHrrf6XV">
                            <field name="TEXT">Hello</field>
                          </shadow>
                          <block type="variables_get" id="pMlIi[01}q5|E1}tV4jV">
                            <field name="VAR" id="FO?PC{-AlDoW3(yAQ!y]" variabletype="">距離</field>
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
                                      <block type="controls_if" id="idqG4s9Yxox?!hSnbi2Z">
                                        <value name="IF0">
                                          <shadow type="logic_boolean" id=")5o|VRBIaQL{=~W],[e@">
                                            <field name="BOOL">TRUE</field>
                                          </shadow>
                                          <block type="logic_compare" id="UNFH`C+PuC.D`F!P2YBj">
                                            <field name="OP">GT</field>
                                            <value name="A">
                                              <block type="dht11temp" id=";a*P`r{v!GX%aGp5YRW#">
                                                <value name="NAME">
                                                  <shadow type="math_number" id="F4+vcGz9W]JYFI4dsR}T">
                                                    <field name="NUM">16</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </value>
                                            <value name="B">
                                              <block type="math_number" id="0p:NJZ=r}_2)kRAx=e}O">
                                                <field name="NUM">33</field>
                                              </block>
                                            </value>
                                          </block>
                                        </value>
                                        <statement name="DO0">
                                          <block type="servowrite" id="nZ-W;u?9z^qXX?z_6:|a">
                                            <value name="pin">
                                              <shadow type="math_number" id="|C^zAxmr:;|Eo6-RT2YL">
                                                <field name="NUM">1</field>
                                              </shadow>
                                            </value>
                                            <value name="value">
                                              <shadow type="math_number" id="!+j^Q?y1lyE)K*s=fB,0">
                                                <field name="NUM">130</field>
                                              </shadow>
                                            </value>
                                            <next>
                                              <block type="digital1" id="0@*Q7b1dfgEf_m)F0zfP">
                                                <value name="pin">
                                                  <shadow type="math_number" id="NAkFk3W@65uNn5)JW[LZ">
                                                    <field name="NUM">17</field>
                                                  </shadow>
                                                </value>
                                                <value name="value">
                                                  <shadow type="math_number" id=":@gMzfe$|e,g!4a9Lq81">
                                                    <field name="NUM">1</field>
                                                  </shadow>
                                                </value>
                                              </block>
                                            </next>
                                          </block>
                                        </statement>
                                        <next>
                                          <block type="controls_if" id="2x@mH+LS^0HXx[sX-9-*">
                                            <comment pinned="true" h="120" w="160">計時a開始</comment>
                                            <value name="IF0">
                                              <shadow type="logic_boolean" id="/r=!^v_9{A7O8Q%xQuaN">
                                                <field name="BOOL">TRUE</field>
                                              </shadow>
                                              <block type="logic_compare" id="FAX@4P5RdSl8Rp.|#x,=">
                                                <field name="OP">EQ</field>
                                                <value name="A">
                                                  <block type="digital2" id="e@80SDLjma!B~532~1bR">
                                                    <value name="pin">
                                                      <shadow type="math_number" id="?u%JUK1(zJf-OpvoXUEo">
                                                        <field name="NUM">17</field>
                                                      </shadow>
                                                    </value>
                                                  </block>
                                                </value>
                                                <value name="B">
                                                  <block type="math_number" id="-1~yb^e1wNzcN/L6:#Z,">
                                                    <field name="NUM">1</field>
                                                  </block>
                                                </value>
                                              </block>
                                            </value>
                                            <statement name="DO0">
                                              <block type="math_change" id="CNjwCoeZL$vlAfWs/F|o">
                                                <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                                <value name="DELTA">
                                                  <shadow type="math_number" id=")ga?MBc|^cJKv}WFztvE">
                                                    <field name="NUM">1</field>
                                                  </shadow>
                                                  <block type="math_arithmetic" id="PLnnH[S#euw-sv/(3aU!">
                                                    <field name="OP">ADD</field>
                                                    <value name="A">
                                                      <shadow type="math_number" id="}OBTl_s`~yA?*=c5EZ*J">
                                                        <field name="NUM">1</field>
                                                      </shadow>
                                                      <block type="variables_get" id="CpO7Zkk3(%-gt1*E+JF.">
                                                        <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                                      </block>
                                                    </value>
                                                    <value name="B">
                                                      <shadow type="math_number" id="t*KsD)Y5t*5mZyVI|NA%">
                                                        <field name="NUM">1</field>
                                                      </shadow>
                                                    </value>
                                                  </block>
                                                </value>
                                                <next>
                                                  <block type="arduinodelay" id="+[{YTKy+}z9cj8|EerK%">
                                                    <value name="value">
                                                      <shadow type="math_number" id="`x8Zr~oLRGhF*~5(7./:">
                                                        <field name="NUM">500</field>
                                                      </shadow>
                                                    </value>
                                                  </block>
                                                </next>
                                              </block>
                                            </statement>
                                            <next>
                                              <block type="controls_if" id="B26mG/Ak2n#I|13K4cgP">
                                                <comment pinned="true" h="120" w="160">計時a結束</comment>
                                                <value name="IF0">
                                                  <shadow type="logic_boolean" id="O*:Qw7nI?Zf]d2B,AYJ2">
                                                    <field name="BOOL">TRUE</field>
                                                  </shadow>
                                                  <block type="logic_compare" id="@.LaOx0`Gp|.#:bDQ^f,">
                                                    <field name="OP">GT</field>
                                                    <value name="A">
                                                      <block type="variables_get" id="h|{42yxF%w#!@i|fEPGd">
                                                        <field name="VAR" id="36q*i(PZk]9GjQ;MqWj3" variabletype="">計時a</field>
                                                      </block>
                                                    </value>
                                                    <value name="B">
                                                      <block type="math_number" id="}b$S[^O7`uBPHvguqQyu">
                                                        <field name="NUM">10</field>
                                                      </block>
                                                    </value>
                                                  </block>
                                                </value>
                                                <statement name="DO0">
                                                  <block type="digital1" id="1]={pINj-C4`U;11pmqt">
                                                    <value name="pin">
                                                      <shadow type="math_number" id="up9;9fxLvfr9bh7X?fzN">
                                                        <field name="NUM">17</field>
                                                      </shadow>
                                                    </value>
                                                    <value name="value">
                                                      <shadow type="math_number" id="0?{wCnwB1`O**V;)bR7?">
                                                        <field name="NUM">0</field>
                                                      </shadow>
                                                    </value>
                                                  </block>
                                                </statement>
                                                <next>
                                                  <block type="controls_if" id="vK.cDTteV7oNZA,,V~7{">
                                                    <comment pinned="true" h="120" w="160">計時b開始</comment>
                                                    <value name="IF0">
                                                      <shadow type="logic_boolean" id="m{DhoDhGS!re%)F;pMh=">
                                                        <field name="BOOL">TRUE</field>
                                                      </shadow>
                                                      <block type="logic_operation" id="I8ItNc97Z5P(R2B+GfP-">
                                                        <field name="OP">AND</field>
                                                        <value name="A">
                                                          <block type="logic_compare" id="M!zfpE_h36MXGBn23PKD">
                                                            <field name="OP">LT</field>
                                                            <value name="A">
                                                              <block type="analog2" id="OVLEOi6:7N/_Ij2eW(od">
                                                                <value name="pin">
                                                                  <shadow type="math_number" id="?1idjbTf+0XaD(]#F./@">
                                                                    <field name="NUM">15</field>
                                                                  </shadow>
                                                                </value>
                                                              </block>
                                                            </value>
                                                            <value name="B">
                                                              <block type="math_number" id="ABFzQ^S*u@oWlD9j4Y3*">
                                                                <field name="NUM">650</field>
                                                              </block>
                                                            </value>
                                                          </block>
                                                        </value>
                                                        <value name="B">
                                                          <block type="logic_compare" id="PX=gzVS)9v_/X7ff{FE$">
                                                            <field name="OP">LT</field>
                                                            <value name="A">
                                                              <block type="variables_get" id="Is2%qPrP2956EDi4?sYM">
                                                                <field name="VAR" id="FO?PC{-AlDoW3(yAQ!y]" variabletype="">距離</field>
                                                              </block>
                                                            </value>
                                                            <value name="B">
                                                              <block type="math_number" id="z((obg6qu|EqE77g`||`">
                                                                <field name="NUM">30</field>
                                                              </block>
                                                            </value>
                                                          </block>
                                                        </value>
                                                      </block>
                                                    </value>
                                                    <statement name="DO0">
                                                      <block type="digital1" id="^@e{ar4W:rD0uOP{~A;d">
                                                        <value name="pin">
                                                          <shadow type="math_number" id="5lh1y`j~ZF!Y6B{g-.*l">
                                                            <field name="NUM">13</field>
                                                          </shadow>
                                                        </value>
                                                        <value name="value">
                                                          <shadow type="math_number" id="U)TE%C#_3e;NQ$!1?KZu">
                                                            <field name="NUM">1</field>
                                                          </shadow>
                                                        </value>
                                                        <next>
                                                          <block type="arduinodelay" id="r0h`-+m#`iAZ2|:q5HC)">
                                                            <value name="value">
                                                              <shadow type="math_number" id="+]Iw/Q@1#!m_:A;|Z;@g">
                                                                <field name="NUM">200</field>
                                                              </shadow>
                                                            </value>
                                                            <next>
                                                              <block type="math_change" id="n4+b2s[+shD28i|yrpn*">
                                                                <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                                                                <value name="DELTA">
                                                                  <shadow type="math_number" id="*yK.5q%wRH(_Kub6z,jN">
                                                                    <field name="NUM">1</field>
                                                                  </shadow>
                                                                  <block type="math_arithmetic" id="C?MYcyyH[clOA;KV~u61">
                                                                    <field name="OP">ADD</field>
                                                                    <value name="A">
                                                                      <shadow type="math_number" id="VTN_=1!fA3uOgwB`WkE/">
                                                                        <field name="NUM">1</field>
                                                                      </shadow>
                                                                      <block type="variables_get" id="ycxVaY%s8WwMVDY6Qh[Y">
                                                                        <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                                                                      </block>
                                                                    </value>
                                                                    <value name="B">
                                                                      <shadow type="math_number" id="Wf/~D_Iu4-JkSbbekWnU">
                                                                        <field name="NUM">1</field>
                                                                      </shadow>
                                                                    </value>
                                                                  </block>
                                                                </value>
                                                              </block>
                                                            </next>
                                                          </block>
                                                        </next>
                                                      </block>
                                                    </statement>
                                                    <next>
                                                      <block type="controls_if" id="%Ye!*[/Cy#?M=YGBEts%">
                                                        <value name="IF0">
                                                          <shadow type="logic_boolean" id="A)jI{:Tu+Ur4vLl??leO">
                                                            <field name="BOOL">TRUE</field>
                                                          </shadow>
                                                          <block type="logic_compare" id="MsNa.0$sw:Cx+F9(ZPV#">
                                                            <field name="OP">GT</field>
                                                            <value name="A">
                                                              <block type="variables_get" id="a=Re!0_u;Kuq21%4e9Zd">
                                                                <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                                                              </block>
                                                            </value>
                                                            <value name="B">
                                                              <block type="math_number" id="(wDWXsvHq5^gaB.E!doF">
                                                                <field name="NUM">20</field>
                                                              </block>
                                                            </value>
                                                          </block>
                                                        </value>
                                                        <statement name="DO0">
                                                          <block type="digital1" id="iaDLs5;=1;yErIswba=U">
                                                            <value name="pin">
                                                              <shadow type="math_number" id="|jxxq^!YWEFPZ1vY/0Q_">
                                                                <field name="NUM">13</field>
                                                              </shadow>
                                                            </value>
                                                            <value name="value">
                                                              <shadow type="math_number" id="YlyJOR4`#DU6awAo.;%;">
                                                                <field name="NUM">0</field>
                                                              </shadow>
                                                            </value>
                                                            <next>
                                                              <block type="math_change" id="ik]KH*`e-Lle?-sEK,=X">
                                                                <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                                                                <value name="DELTA">
                                                                  <shadow type="math_number" id="E1dB7Z`+-+h@OTgZu%u2">
                                                                    <field name="NUM">0</field>
                                                                  </shadow>
                                                                </value>
                                                              </block>
                                                            </next>
                                                          </block>
                                                        </statement>
                                                        <next>
                                                          <block type="controls_if" id="r_M[Tq7?]3)#2m-WPi3g">
                                                            <comment pinned="true" h="120" w="160">計時b結束</comment>
                                                            <value name="IF0">
                                                              <shadow type="logic_boolean" id="lMOTyWdw_|KruM07oOP:">
                                                                <field name="BOOL">TRUE</field>
                                                              </shadow>
                                                              <block type="logic_compare" id="Ds7yi]B~2Bb?y/a-uT`=">
                                                                <field name="OP">GT</field>
                                                                <value name="A">
                                                                  <block type="analog2" id="pu(.~;:7[fes=/(Uasu~">
                                                                    <value name="pin">
                                                                      <shadow type="math_number" id="h8fht}btxh^Za%:uX3cf">
                                                                        <field name="NUM">15</field>
                                                                      </shadow>
                                                                    </value>
                                                                  </block>
                                                                </value>
                                                                <value name="B">
                                                                  <block type="math_number" id="jd6Q/t|u~xQ8114|My--">
                                                                    <field name="NUM">650</field>
                                                                  </block>
                                                                </value>
                                                              </block>
                                                            </value>
                                                            <statement name="DO0">
                                                              <block type="digital1" id="|-h?4ogzZsC6s%c9}2j~">
                                                                <value name="pin">
                                                                  <shadow type="math_number" id="de.M+;mr6.:HQ)$=5{eY">
                                                                    <field name="NUM">13</field>
                                                                  </shadow>
                                                                </value>
                                                                <value name="value">
                                                                  <shadow type="math_number" id="ji|`g9Na=dUVvg%.)0tq">
                                                                    <field name="NUM">0</field>
                                                                  </shadow>
                                                                </value>
                                                                <next>
                                                                  <block type="math_change" id="5[1b42`}f=`1+,i-UR=-">
                                                                    <field name="VAR" id="!bo:M9uNNy?bl6VZt;mY" variabletype="">計時b</field>
                                                                    <value name="DELTA">
                                                                      <shadow type="math_number" id="2S#oTr=Y@-f;~MxiEIee">
                                                                        <field name="NUM">0</field>
                                                                      </shadow>
                                                                    </value>
                                                                  </block>
                                                                </next>
                                                              </block>
                                                            </statement>
                                                            <next>
                                                              <block type="math_change" id="z#wG%i%E__)$)TRb1~@u">
                                                                <field name="VAR" id="FO?PC{-AlDoW3(yAQ!y]" variabletype="">距離</field>
                                                                <value name="DELTA">
                                                                  <shadow type="math_number" id="qD0Xn`yQc2gIvW!~=kT.">
                                                                    <field name="NUM">1</field>
                                                                  </shadow>
                                                                  <block type="aultrasound" id="dnpfxpGz,6zo[$rQIP#d">
                                                                    <value name="pin">
                                                                      <shadow type="math_number" id="kW|$N6-ngO4m3mXi=Vv#">
                                                                        <field name="NUM">2</field>
                                                                      </shadow>
                                                                    </value>
                                                                    <value name="pin1">
                                                                      <shadow type="math_number" id="xB]$jLyGw2[tb)GZc)e|">
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