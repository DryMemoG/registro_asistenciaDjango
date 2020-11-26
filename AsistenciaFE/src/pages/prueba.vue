<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="height: 80vh; width: 65vw">
      <div class="row">
        <div class="col">
          <q-input label="Buscar" @keyup="search" v-model="search_text" />
        </div>
        <div class="col-2">
          <q-btn flat color="primary" label="Ver préstamos" to="/ActiveLoans"/>
        </div>
      </div>
      <div
        v-if="books[0].length == 0"
        class="flex flex-center"
        style="height: 63vh;"
      >
        No hay coincidencias
      </div>
      <div
        class="row q-pa-md"
        v-for="(book_row, index) in books"
        v-bind:key="index"
      >
        <q-card
          class="my-card"
          v-for="(book, index1) in book_row"
          v-bind:key="index1"
          style="width:20vw; height: 30vh;"
        >
          <q-card-section>
            <div class="text-h5 text-bold">{{ book.node.title }}</div>
            <div class="text-h6" style="color:gray">Autores</div>
            <q-scroll-area style="height: 10vh; max-width: 20vw;">
              <div
                v-for="(author, index) in book.node.author"
                v-bind:key="index"
                class="q-pa-xs"
              >
                {{ author.name }}
              </div>
            </q-scroll-area>
            <div class="row">
              <div class="text-subtitle2 col">
                Disponibles: {{ book.node.existence }}
              </div>
              <div class="col">
                <q-btn
                  label="Prestar"
                  color="black"
                  :disable="book.node.existence == 0"
                  @click="loanBook(book.node)"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
    <!--LOAN DIALOG-->
    <q-dialog v-model="loan_dialog">
      <q-card class="my-card q-pa-md" style="width: 100%; height: 80vh">
        <div class="text-h4">{{ current_book.title }}</div>
        <div class="text-h6">Autores</div>
        <div
          v-for="(author, index) in current_book.author"
          v-bind:key="index"
          class="q-pa-xs"
        >
          {{ author.name }}
        </div>
        <q-separator />
        <br />
        <div class="text-h6">Usuarios disponibles</div>
        <q-select
          v-model="loan_info.user"
          :options="loan_users"
          label="Usuarios"
        />
        <div class="text-h6">Cantidad de ejemplares</div>
        <q-input
          v-model="loan_info.quantity"
          type="number"
          min="1"
          :max="current_book.existence"
        />
        <div class="text-h6">Fecha de retorno</div>
        <center>
          <q-date v-model="loan_info.date" />
        </center>
        <br />
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="red" v-close-popup />
          <q-btn flat label="Guardar" color="green" @click="save_loan" />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <Dialog
      :active="dialog.active"
      :title="dialog.title"
      :body="dialog.body"
      :icon="dialog.icon"
      :color="dialog.color"
      :close="close_popup"
    />
  </q-page>
</template>

<script>
import Dialog from "./Dialog";
export default {
  components: {
    Dialog
  },
  data() {
    return {
      books: [],
      all_books: [],
      search_text: null,
      current_book: {},
      loan_dialog: false,
      loan_users: [],
      loan_info: {
        user: null,
        book: null,
        date: new Date()
          .toJSON()
          .slice(0, 10)
          .replace(/-/g, "/"),
        quantity: 0
      },
      dialog: {
        active: false,
        title: "",
        body: "",
        icon: "",
        color: ""
      }
    };
  },
  methods: {
    async save_loan() {
      const query = `
            mutation createLoan ($book: String!, $finishdate: String!, $userclient: String!, $quantity: String!) {
                createLoan(book: $book, finishdate: $finishdate, userclient: $userclient, quantity: $quantity){
                    loan{
                        id
                    }
                }
            }`,
        variables = {
          book: this.loan_info.book,
          finishdate: this.loan_info.date.replaceAll("/", "-"),
          userclient: this.loan_info.user.value,
          quantity: this.loan_info.quantity
        };
        console.log(query, variables)
      const data = await this.$graphql(query, variables);
      if (data.message == "OK" && data.data) {
        if (data.data.createLoan) {
          //IF BRINGS DATA
          this.dialog.title = "Completado";
          this.dialog.body = "El préstamo se ha realizado correctamente.";
          this.dialog.icon = "check_box";
          this.dialog.color = "green";
          this.dialog.active = true;
          location.reload();
        } else {
          //IF IS NULL FOR SOME SERVER ERROR
          this.dialog.title = "Error";
          this.dialog.body =
            "El préstamo no se ha podido realizar, intentelo nuevamente.";
          this.dialog.icon = "error";
          this.dialog.color = "red";
          this.dialog.active = true;
        }
      } else if (data.message == "ERROR" || data.data == undefined) {
        this.dialog.title = "Error";
        this.dialog.body =
          "El préstamo no se ha podido realizar, intentelo nuevamente (SERV).";
        this.dialog.icon = "error";
        this.dialog.color = "red";
        this.dialog.active = true;
      }
    },
    async loanBook(book_info) {
      this.current_book = book_info;
      const query = `
      query {
        allUsers{
          edges {
            node {
              id
              firstName
              lastName
              username
              groups {
                id
                name
              }
            }
          }
        }
      }
      `,
        data = await this.$graphql(query, {});
      if (data.data.allUsers) {
        const users = data.data.allUsers.edges;
        this.loan_users = []
        users.forEach(user => {
          if (user.node.groups.some(group => group.name === "client")) {
            this.loan_users.push({
              value: user.node.username,
              label: user.node.firstName + " " + user.node.lastName + " - " + user.node.username
            });
          }
        });
        this.loan_info.book = book_info.title;
        this.loan_dialog = true;
      }
    },
    search() {
      if (this.search_text && this.search_text != "") {
        var temp_arr = [],
          cont = 0,
          reg = new RegExp(".*" + this.search_text + ".*", "i");
        this.books = [];
        this.all_books.forEach(arr => {
          arr.forEach(book => {
            if (
              reg.test(book.node.title) ||
              book.node.author.some(info => reg.test(info.name))
            ) {
              if (cont == 3) {
                cont = 0;
                this.books.push(temp_arr);
                temp_arr = [book];
              } else {
                temp_arr.push(book);
              }
              cont++;
            }
          });
        });
        this.books.push(temp_arr);
      } else {
        this.books = this.all_books;
      }
    },
    close_popup() {
      this.dialog.active = false;
    }
  },
  async created() {
    //this.$q.loading.show();
    const query = `
    query {
        allBooks {
            edges {
                node {
                    id
                    title
                    description
                    existence
                    author {
                        name
                    }
                }
            }
        }
    }
    `;
    const data = await this.$graphql(query, {});
    if (data.data.allBooks) {
      var temp_arr = [],
        cont = 0;
      data.data.allBooks.edges.forEach(book => {
        if (cont == 3) {
          cont = 0;
          this.books.push(temp_arr);
          temp_arr = [book];
        } else {
          temp_arr.push(book);
        }
        cont++;
      });
      this.books.push(temp_arr);
      this.all_books = this.books;
    }
  }
};
</script>
