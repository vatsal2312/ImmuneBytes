// This is a class used for encryption of the user's predictions.
export default class Encoding {
    constructor() {
        this.A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
    }

    byteToHexString (uint8arr) {
        if (!uint8arr) {
          return '';
        }
        
        var hexStr = '';
        for (var i = 0; i < uint8arr.length; i++) {
          var hex = (uint8arr[i] & 0xff).toString(16);
          hex = (hex.length === 1) ? '0' + hex : hex;
          hexStr += hex;
        }
        
        return hexStr.toUpperCase();
    }

    hexStringToByte(str) {
        if (!str) {
          return new Uint8Array();
        }
        
        var a = [];
        for (var i = 0, len = str.length; i < len; i += 2) {
          a.push(parseInt(str.substr(i, 2), 16));
        }
        
        return new Uint8Array(a);
    }

    byteToB58(B) {
        var d = [], s = "", i, j, c, n;        
        for(i in B) { 
            j = 0,                           
            c = B[i];                        
            s += c || s.length ^ i ? "" : 1; 
            while(j in d || c) {             
                n = d[j];                    
                n = n ? n * 256 + c : c;     
                c = n / 58 | 0;              
                d[j] = n % 58;               
                j++;         
            }
        }
        while(j--)
            s += this.A[d[j]];
        return s;
    }
    
    b58ToByte(S) {
        this.A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
        var d = [], b = [], i, j, c, n;
        for(i in S) {
            j = 0,
            c = this.A.indexOf( S[i] );
            if(c < 0)
                return undefined;
            c || b.length ^ i ? i : b.push(0);
            while(j in d || c) {
                n = d[j];
                n = n ? n * 58 + c : c;
                c = n >> 8;
                d[j] = n % 256;
                j++;
            }
        }
        while(j--)
            b.push(d[j]);
        return new Uint8Array(b);
    }
}
